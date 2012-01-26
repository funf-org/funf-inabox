package funfinabox.__ID__;

import java.io.File;

import android.content.Context;

import edu.mit.media.funf.storage.RemoteArchive;

public class DropboxArchive implements RemoteArchive {
	
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
		// TODO Auto-generated method stub
		return "dropbox://funfinabox/__ID__";
	}

}
