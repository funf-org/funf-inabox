package funfinabox.__ID__;

import static funfinabox.__ID__.Info.TAG;
import static edu.mit.media.funf.AsyncSharedPrefs.async;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.Charset;
import java.util.ArrayList;

import org.json.JSONException;

import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import edu.mit.media.funf.IOUtils;
import edu.mit.media.funf.Utils;
import edu.mit.media.funf.configured.ConfiguredPipeline;
import edu.mit.media.funf.configured.FunfConfig;
import edu.mit.media.funf.probe.Probe;
import edu.mit.media.funf.probe.ProbeUtils;
import edu.mit.media.funf.storage.BundleSerializer;


public class DropboxPipeline extends ConfiguredPipeline{

	
	
	public static final String MAIN_CONFIG = "main_config";
	public static final String BACKUP_CONFIG = "backup_config";
	public static final String ONE_TIME_REQUEST_ID = "ONE_TIME";
	public static final String ACTION_RUN_ONCE = "RUN_ONCE";
	public static final String RUN_ONCE_PROBE_NAME = "PROBE_NAME";
	
	@Override
	public void onCreate() {
		super.onCreate();
		Log.i(TAG, "Main Pipeline CREATED!");
	}
	
	@Override
	public void onDataReceived(Bundle data) {
		super.onDataReceived(data);
	}

	@Override
	protected void onHandleIntent(Intent intent) {
		if (ACTION_RUN_ONCE.equals(intent.getAction())) {
			String probeName = intent.getStringExtra(RUN_ONCE_PROBE_NAME);
			runProbeOnceNow(this, probeName);
		} else {
			super.onHandleIntent(intent);
		}
	}
	

	

	@Override
	public void updateConfig() {
		// TODO Auto-generated method stub
		super.updateConfig();
	}

	@Override
	public void uploadData() {
		// TODO Auto-generated method stub
		super.uploadData();
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
