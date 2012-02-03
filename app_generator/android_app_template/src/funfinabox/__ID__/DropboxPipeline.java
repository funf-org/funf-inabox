package funfinabox.__ID__;

import static edu.mit.media.funf.AsyncSharedPrefs.async;
import static funfinabox.__ID__.Info.TAG;

import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.nio.charset.Charset;
import java.util.ArrayList;

import org.json.JSONException;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.app.PendingIntent.CanceledException;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import edu.mit.media.funf.IOUtils;
import edu.mit.media.funf.Utils;
import edu.mit.media.funf.configured.ConfiguredPipeline;
import edu.mit.media.funf.configured.FunfConfig;
import edu.mit.media.funf.probe.Probe;
import edu.mit.media.funf.storage.BundleSerializer;
import edu.mit.media.funf.storage.UploadService;


public class DropboxPipeline extends ConfiguredPipeline{

	
	
	public static final String MAIN_CONFIG = "main_config";
	public static final String BACKUP_CONFIG = "backup_config";
	public static final String ONE_TIME_REQUEST_ID = "ONE_TIME";
	public static final String ACTION_RUN_ONCE = "RUN_ONCE";
	public static final String RUN_ONCE_PROBE_NAME = "PROBE_NAME";
	
	/// HACK USED TO OVERRIDE BUG #78
	public void ensureServicesAreRunning() {
		Log.i(TAG, "DropboxPipeline ensuring services are running");
		if (isEnabled()) {
			scheduleAlarms();
			sendProbeRequests();
		}
	}
	private void scheduleAlarms() {
		Log.i(TAG, "DropboxPipeline scheduling alarms");
		FunfConfig config = getConfig();
		scheduleAlarm(ACTION_UPDATE_CONFIG, config.getConfigUpdatePeriod());
		scheduleAlarm(ACTION_ARCHIVE_DATA, config.getDataArchivePeriod());
		scheduleAlarm(ACTION_UPLOAD_DATA, config.getDataUploadPeriod());
	}
	
	private void scheduleAlarm(String action, long delayInSeconds) {
		Log.i(TAG, "DropboxPipeline scheduling alarm for " + action + " in " + delayInSeconds + " seconds");
		Intent i = new Intent(this, getClass());
		i.setAction(action);
		Log.i(TAG, "DropboxPipeline intent info " + i.getComponent() + " " + i.getAction());
		boolean noAlarmExists = (PendingIntent.getService(this, 0, i, PendingIntent.FLAG_NO_CREATE) == null);
		if (noAlarmExists) {
			PendingIntent pi = PendingIntent.getService(this, 0, i, PendingIntent.FLAG_UPDATE_CURRENT);
			Log.i(TAG, "DropboxPipeline pi info " + pi.toString());
			try {
				pi.send();
			} catch (CanceledException e) {
				Log.i(TAG, "DropboxPipeline pi was cancelled");
			}
			AlarmManager alarmManager = (AlarmManager)getSystemService(ALARM_SERVICE);
			long delayInMilliseconds = Utils.secondsToMillis(delayInSeconds);
			long startTimeInMilliseconds = System.currentTimeMillis() + delayInMilliseconds;
			Log.i(TAG, "Scheduling alarm for '" + action + "' at " + Utils.millisToSeconds(startTimeInMilliseconds) + " and every " + delayInSeconds  + " seconds");
			// Inexact repeating doesn't work unlesss interval is 15, 30 min, or 1, 6, or 24 hours
			alarmManager.setRepeating(AlarmManager.RTC_WAKEUP, startTimeInMilliseconds, delayInMilliseconds, pi);
		} else {
			Log.i(TAG, "DropboxPipeline alarm already exists");
		}
	}
	
	public void onSharedPreferenceChanged (SharedPreferences sharedPreferences, String key) {
		Log.i(TAG, "Shared Prefs changed");
		if (sharedPreferences.equals(getConfig().getPrefs())) {
			Log.i(TAG, "Configuration changed");
			onConfigChange(getConfig().toString(true));
			if (FunfConfig.isDataRequestKey(key)) {
				if (isEnabled()) {
					String probeName = FunfConfig.keyToProbename(key);
					sendProbeRequest(probeName);
				}
			} else if (FunfConfig.CONFIG_UPDATE_PERIOD_KEY.equals(key)) {
				cancelAlarm(ACTION_UPDATE_CONFIG);
			} else if (FunfConfig.DATA_ARCHIVE_PERIOD_KEY.equals(key)) {
				cancelAlarm(ACTION_ARCHIVE_DATA);
			} else if (FunfConfig.DATA_UPLOAD_PERIOD_KEY.equals(key)) {
				cancelAlarm(ACTION_UPLOAD_DATA);
			}
			if (isEnabled()) {
				scheduleAlarms();
			}
			
		} else if (sharedPreferences.equals(getSystemPrefs()) && ENABLED_KEY.equals(key)) {
			Log.i(TAG, "System prefs changed");
			reload();
		}
	}
	
	public void reload() {
		cancelAlarms();
		super.reload();
	}
	
	private void cancelAlarms() {
		cancelAlarm(ACTION_UPDATE_CONFIG);
		cancelAlarm(ACTION_ARCHIVE_DATA);
		cancelAlarm(ACTION_UPLOAD_DATA);
	}
	
	private void cancelAlarm(String action) {
		Intent i = new Intent(this, getClass());
		i.setAction(action);
		PendingIntent pi = PendingIntent.getService(this, 0, i, PendingIntent.FLAG_NO_CREATE);
		if (pi != null) {
			AlarmManager alarmManager = (AlarmManager)getSystemService(ALARM_SERVICE);
			alarmManager.cancel(pi);
			pi.cancel();
		}
	}
	/////////////////////////////
	
	@Override
	public void onCreate() {
		super.onCreate();
		Log.i(TAG, "Main Pipeline CREATED!");
		setEncryptionPassword("__PASSWORD__".toCharArray());
		
		// One time upload of data 2 minutes after initial load
		Intent i = new Intent(this, getClass());
		i.setAction(ACTION_UPLOAD_DATA);
		i.setData(Uri.parse("sample://unused_data")); // Used to make sure we don't capture the real scheduled pending intent
		PendingIntent pi = PendingIntent.getService(this, 0, i, PendingIntent.FLAG_UPDATE_CURRENT);
		AlarmManager alarmManager = (AlarmManager)getSystemService(ALARM_SERVICE);
		alarmManager.set(AlarmManager.RTC_WAKEUP, Utils.secondsToMillis(120), pi);
	}
	
	@Override
	public void onDataReceived(Bundle data) {
		super.onDataReceived(data);
	}

	@Override
	protected void onHandleIntent(Intent intent) {
		Log.i(TAG, "DropboxPipeline intent: " + intent.getAction());
		if (ACTION_RUN_ONCE.equals(intent.getAction())) {
			String probeName = intent.getStringExtra(RUN_ONCE_PROBE_NAME);
			runProbeOnceNow(this, probeName);
		} else {
			super.onHandleIntent(intent);
		}
	}
	

	

	@Override
	public void updateConfig() {
		String config = DropboxUtil.getConfig(this);
		super.updateConfig(config);
	}

	@Override
	public void uploadData() {
		Log.i(TAG, "Dropbox pipeline launching Upload");
		archiveData();
		String archiveName = getPipelineName();
		String uploadUrl = DropboxArchive.DROPBOX_ID;
		Intent i = new Intent(this, getUploadServiceClass());
		i.putExtra(UploadService.ARCHIVE_ID, archiveName);
		i.putExtra(UploadService.REMOTE_ARCHIVE_ID, uploadUrl);
		startService(i);
		getSystemPrefs().edit().putLong(LAST_DATA_UPLOAD, System.currentTimeMillis()).commit();
	}
	
	@Override
	public Class<? extends UploadService> getUploadServiceClass() {
		return DropboxUploadService.class;
	}

	@Override
	public void onDestroy() {
		super.onDestroy();
	}



	@Override
	public BundleSerializer getBundleSerializer() {
		return new BundleToJson();
	}
	
	public static class BundleToJson implements BundleSerializer {
		public String serialize(Bundle bundle) {
			return JsonUtils.getGson().toJson(Utils.getValues(bundle));
		}
		
	}
	
	@Override
	public SharedPreferences getSystemPrefs() {
		return getMainSystemPrefs(this);
	}
	
	public static SharedPreferences getMainSystemPrefs(Context context) {
		return async(context.getSharedPreferences(DropboxPipeline.class + "_system", MODE_PRIVATE));
	}
	
	@Override
	public FunfConfig getConfig() {
		return getMainConfig(this);
	}

	private static FunfConfig configInstance;
	/**
	 * Easy access to Funf config.  
	 * As long as this service is running, changes will be automatically picked up.
	 * @param context
	 * @return
	 */
	public static FunfConfig getMainConfig(Context context) {
		if (configInstance == null) {
			synchronized (DropboxPipeline.class) {
				if (configInstance == null) {
					configInstance = getConfig(context, MAIN_CONFIG);
					if (configInstance.getName() == null) {			
						resetConfig(context, configInstance);
					}
				}
			}
		}
		return configInstance;
	}
	
	private static FunfConfig backupConfigInstance;
	/**
	 * Backup funf config to store data requests when they are disabled.  That way they can be easily restored.
	 * @param context
	 * @return
	 */
	public static FunfConfig getBackupConfig(Context context) {
		if (backupConfigInstance == null) {
			synchronized (DropboxPipeline.class) {
				if (backupConfigInstance == null) {
					backupConfigInstance = getConfig(context, BACKUP_CONFIG);
				}
			}
		}
		return backupConfigInstance;
	}
	
	public static void resetConfig(Context context, FunfConfig config) {
		String jsonString = context.getString(R.string.config);
		//String jsonString = getStringFromAsset(context, "default_config.json");
		if (jsonString == null) {
			Log.e(TAG, "Error loading default config.  Using blank config.");
			jsonString = "{}";
		}
		try {
			getMainConfig(context).edit().setAll(jsonString).commit();
			getBackupConfig(context).edit().clear().commit();
		} catch (JSONException e) {
			Log.e(TAG, "Error parsing default config", e);
		}
	}
	
	public static String getStringFromAsset(Context context, String filename) {
		InputStream is = null;
		try {
			is = context.getAssets().open(filename);
			return IOUtils.inputStreamToString(is, Charset.defaultCharset().name());
		} catch (IOException e) {
			Log.e(TAG, "Unable to read asset to string", e);
			return null;
		} finally {
			if (is != null) {
				try {
					is.close();
				} catch (IOException e) {
					Log.e(TAG, "Unable to close asset input stream", e);
				}
			}
		}
	}

	public void runProbeOnceNow(final Context context, final String probeName) {
		FunfConfig config = getMainConfig(context);
		ArrayList<Bundle> updatedRequests = new ArrayList<Bundle>();
		Bundle[] existingRequests = config.getDataRequests(probeName);
		if (existingRequests != null) {
			for (Bundle existingRequest : existingRequests) {
				updatedRequests.add(existingRequest);
			}
		}
		
		Bundle oneTimeRequest = new Bundle();
		oneTimeRequest.putLong(Probe.Parameter.Builtin.PERIOD.name, 0L);
		updatedRequests.add(oneTimeRequest);
		
		Intent request = new Intent(Probe.ACTION_REQUEST);
		request.setClassName(this, probeName);
		request.putExtra(Probe.CALLBACK_KEY, getCallback());
		request.putExtra(Probe.REQUESTS_KEY, updatedRequests);
		startService(request);
	}

}
