/**
 * 
 * Funf: Open Sensing Framework
 * Copyright (C) 2010-2011 Nadav Aharony, Wei Pan, Alex Pentland.
 * Acknowledgments: Alan Gardner
 * Contact: nadav@media.mit.edu
 * 
 * This file is part of Funf.
 * 
 * Funf is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as
 * published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version.
 * 
 * Funf is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU Lesser General Public License for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public
 * License along with Funf. If not, see <http://www.gnu.org/licenses/>.
 * 
 */
package funfinabox.__ID__;

import java.io.File;

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.NetworkInfo.State;
import edu.mit.media.funf.config.Configurable;
import edu.mit.media.funf.storage.RemoteFileArchive;

public class DropboxArchive implements RemoteFileArchive {
	
	public static final String DROPBOX_ID = "dropbox://funfinabox/__ID__";
	
    @Configurable
    private boolean wifiOnly = false;
	
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

    @Override
    public boolean isAvailable() {
      assert context != null;
      ConnectivityManager connectivityManager = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
      NetworkInfo netInfo = connectivityManager.getActiveNetworkInfo();
      if (!wifiOnly && netInfo != null && netInfo.isConnectedOrConnecting()) {
        return true;
      } else if (wifiOnly) {
        State wifiInfo = connectivityManager.getNetworkInfo(ConnectivityManager.TYPE_WIFI).getState();
        if (State.CONNECTED.equals(wifiInfo) || State.CONNECTING.equals(wifiInfo)) {
          return true;
        }
      }
      return false;
    }
    

}
