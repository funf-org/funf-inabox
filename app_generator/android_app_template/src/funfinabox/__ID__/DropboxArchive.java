package funfinabox.__ID__;

import java.io.File;

import android.content.Context;

import edu.mit.media.funf.storage.RemoteArchive;

public class DropboxArchive implements RemoteArchive {
	
	public static final String DROPBOX_ID = "dropbox://funfinabox/__ID__";
	
	private Context context;
	
	public DropboxArchive(Context context) {
		this.context = context;
	}
	
	@Override
	public boolean add(File file) {
		return DropboxUtil.uploadDataFile(context, file);
	}

	@Override
	public String getId() {
		return DROPBOX_ID;
	}

}
