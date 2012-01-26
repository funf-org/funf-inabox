package funfinabox.__ID__;

import edu.mit.media.funf.storage.RemoteArchive;
import edu.mit.media.funf.storage.UploadService;

public class DropboxUploadService extends UploadService {

	@Override
	protected RemoteArchive getRemoteArchive(String id) {
		return new DropboxArchive(getApplicationContext());
	}

}
