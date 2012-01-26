package funfinabox.__ID__;

import static funfinabox.__ID__.Info.TAG;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.UnsupportedEncodingException;

import android.content.Context;
import android.util.Log;

import com.dropbox.client2.DropboxAPI;
import com.dropbox.client2.android.AndroidAuthSession;
import com.dropbox.client2.exception.DropboxException;
import com.dropbox.client2.session.AccessTokenPair;
import com.dropbox.client2.session.AppKeyPair;
import com.dropbox.client2.session.Session.AccessType;

public class DropboxUtil {

	static final String 
		APP_KEY = "__DROPBOX_APP_KEY__",
		APP_SECRET = "__DROPBOX_APP_SECRET__",
		APP_TOKEN = "__DROPBOX_TOKEN__",
		APP_TOKEN_SECRET = "__DROPBOX_TOKEN_SECRET__";
	final static private AccessType ACCESS_TYPE = AccessType.APP_FOLDER;
	
	private static DropboxAPI<AndroidAuthSession> dropboxApi;
	public static DropboxAPI<AndroidAuthSession> getDropboxApi() {
		if (dropboxApi == null) {
			AppKeyPair appKeyPair = new AppKeyPair(APP_KEY, APP_SECRET);
			AccessTokenPair accessToken = new AccessTokenPair(APP_TOKEN, APP_TOKEN_SECRET);
			AndroidAuthSession session = new AndroidAuthSession(appKeyPair, ACCESS_TYPE, accessToken);
			dropboxApi = new DropboxAPI<AndroidAuthSession>(session);
		}
        return dropboxApi;
	}
	
	public static String getAppFolder(Context context) {
		return "/" + context.getString(R.string.app_name);
	}
	
	public static String getConfig(Context context) {
		String configFilePath = getAppFolder(context) + "/config/funf_config.json";
		ByteArrayOutputStream os = new ByteArrayOutputStream();
		try {
			getDropboxApi().getFile(configFilePath, null, os, null);
		} catch (DropboxException e) {
			return null;
		}
		try {
			return os.toString("UTF8");
		} catch (UnsupportedEncodingException e) {
			throw new RuntimeException("UTF8 Encoding not supported");
		}
	}
	
	public static boolean uploadDataFile(Context context, File file) {
		String dataPath = getAppFolder(context) + "/data/raw/" + file.getName();
		FileInputStream is = null;
		try {
			is = new FileInputStream(file);
			getDropboxApi().putFileOverwrite(dataPath, is, file.length(), null);
			return true;
		} catch (FileNotFoundException e) {
			Log.w(TAG, "File not found: " + file.getAbsolutePath());
		} catch (DropboxException e) {
			Log.w(TAG, "Dropbox exception: " + file.getAbsolutePath(), e);
		} finally {
			if (is != null) {
				try {
					is.close();
				} catch (IOException e) {
					Log.w(TAG, "Unable to close file: " + file.getAbsolutePath());
				}
			}
		}
		return false;
	}
}
