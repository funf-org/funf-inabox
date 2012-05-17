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

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.text.method.LinkMovementMethod;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;


public class Info extends Activity
{
	public static final String TAG = "__ID__";
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        if (!LauncherReceiver.isLaunched()) {
        	LauncherReceiver.launch(this);
        }
        
        ((TextView)findViewById(R.id.contact_email)).setMovementMethod(LinkMovementMethod.getInstance());
        
        ((Button)findViewById(R.id.uninstall_button)).setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View v) {
				Uri packageURI = Uri.parse("package:" + getPackageName());
				Intent uninstallIntent = new Intent(Intent.ACTION_DELETE, packageURI);
				startActivity(uninstallIntent);
			}
		});
        
        ((ImageView)findViewById(R.id.logo_button)).setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View v) {
				String url = "http://www.funf.org/inabox/";  
				Intent i = new Intent(Intent.ACTION_VIEW);  
				i.setData(Uri.parse(url));  
				startActivity(i);  
			}
		});
    }
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.actions, menu);
        return true;
    }
    
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.sync:
            	syncNow();
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }
    
    private void syncNow() {
    	Context context = getApplicationContext();
    	Toast.makeText(context, R.string.syncing_message, Toast.LENGTH_SHORT).show();
    	
    	Intent updateConfigIntent = new Intent(context, DropboxPipeline.class);
    	updateConfigIntent.setAction(DropboxPipeline.ACTION_UPDATE_CONFIG);
    	startService(updateConfigIntent);
    	
    	Intent uploadDataIntent = new Intent(context, DropboxPipeline.class);
    	uploadDataIntent.setAction(DropboxPipeline.ACTION_UPLOAD_DATA);
    	uploadDataIntent.putExtra(DropboxPipeline.EXTRA_FORCE_UPLOAD, true);
    	startService(uploadDataIntent);
    }
}
