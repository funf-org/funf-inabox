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
package funfinabox.app;

import java.util.ArrayList;
import java.util.List;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.ComponentName;
import android.content.Context;
import android.content.DialogInterface;
import android.content.DialogInterface.OnCancelListener;
import android.content.Intent;
import android.content.ServiceConnection;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
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

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.JsonSyntaxException;

import edu.mit.media.funf.FunfManager;
import edu.mit.media.funf.Launcher;
import edu.mit.media.funf.config.RuntimeTypeAdapterFactory;
import edu.mit.media.funf.pipeline.BasicPipeline;
import edu.mit.media.funf.pipeline.Pipeline;
import edu.mit.media.funf.probe.Probe.DisplayName;
import edu.mit.media.funf.util.StringUtil;
import funfinabox.__ID__.R;


public class Info extends Activity
{
	public static final String TAG = "__ID__";
	public static final String PIPELINE_NAME = "default";
	
	private Handler mainHandler;
	private FunfManager funfMgr = null;
	private Pipeline pipeline = null;
	private ServiceConnection funfMgrConn = new ServiceConnection() {
      
      @Override
      public void onServiceConnected(ComponentName name, IBinder service) {
        funfMgr = ((FunfManager.LocalBinder)service).getManager();
        pipeline = funfMgr.getRegisteredPipeline(TAG);
        if (pipeline == null) {
          new AlertDialog.Builder(Info.this)
          .setTitle("Collect data?")
          .setIcon(android.R.drawable.ic_dialog_info)
          .setCancelable(false)
          .setMessage("This app will collect data from your phone.  Do you want to coninue?")
          .setPositiveButton("Yes", new Dialog.OnClickListener() {
            
            @Override
            public void onClick(DialogInterface dialog, int which) {
              dialog.dismiss();
              boolean success = false;
              try {
                JsonObject configObject = new JsonParser().parse("__CONFIG__").getAsJsonObject();
                success = funfMgr.saveAndReload(PIPELINE_NAME, configObject);
              } catch (JsonSyntaxException e) {
                success = false;
              }
              if(success) {
                pipeline = funfMgr.getRegisteredPipeline(PIPELINE_NAME);
                mainHandler.postDelayed(new Runnable() {
                  @Override
                  public void run() {
                    pipeline.onRun(BasicPipeline.ACTION_ARCHIVE, null);
                    pipeline.onRun(BasicPipeline.ACTION_UPLOAD, null);
                  }
                }, 10L * 1000L);
                reloadProbeList();
              } else {
                String email = getResources().getString(R.string.contact_email);
                new AlertDialog.Builder(Info.this)
                .setTitle("Bad Config!")
                .setIcon(android.R.drawable.ic_dialog_alert)
                .setCancelable(true)
                .setOnCancelListener(new OnCancelListener() {
                  @Override
                  public void onCancel(DialogInterface dialog) {
                    finish();
                  }
                })
                .setMessage("This app has a bad configuration.  Contact " + email )
                .create().show();
              }
            }
          })
          .setNegativeButton("No", new Dialog.OnClickListener() {
            
            @Override
            public void onClick(DialogInterface dialog, int which) {
              dialog.dismiss();
              finish();
            }
          })
          .create().show();
        } else {
          reloadProbeList();
        }
      }
	  
      @Override
      public void onServiceDisconnected(ComponentName name) {
        funfMgr = null;
      }
    };
    
    private void reloadProbeList() {
      // Load probe list view from config
      if (pipeline != null && pipeline instanceof BasicPipeline) {
        List<String> names = new ArrayList<String>();
        for (JsonElement el : ((BasicPipeline)pipeline).getDataRequests()) {
          String probeClassName = el.isJsonPrimitive() ? el.getAsString() : el.getAsJsonObject().get(RuntimeTypeAdapterFactory.TYPE).getAsString();
          DisplayName probeDisplayName = null;
          try {
            probeDisplayName = Class.forName(probeClassName).getAnnotation(DisplayName.class);
          } catch (ClassNotFoundException e) {
            
          }
          String name = "Unknown";
          if (probeDisplayName == null) {
            String[] parts = probeClassName.split(".");
            name = parts[parts.length - 1].replace("Probe", "");
          } else {
            name = probeDisplayName.value();
          }
          names.add(name);
        }
        ((TextView)findViewById(R.id.probe_list)).setText(StringUtil.join(names, ", "));
      } else {
        ((TextView)findViewById(R.id.probe_list)).setText("Unknown...");
      }
      
    }
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        this.mainHandler = new Handler();
        
        if (!Launcher.isLaunched()) {
        	Launcher.launch(this);
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
        
        bindService(new Intent(this, FunfManager.class), funfMgrConn, BIND_AUTO_CREATE);
    }
    
    @Override
    protected void onDestroy() {
      super.onDestroy();
      unbindService(funfMgrConn);
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
    	if (funfMgr == null) {
          Toast.makeText(context, R.string.unable_to_sync, Toast.LENGTH_SHORT).show();
    	} else {
    	  Toast.makeText(context, R.string.syncing_message, Toast.LENGTH_SHORT).show();
          pipeline.onRun(BasicPipeline.ACTION_UPDATE, null);
          pipeline.onRun(BasicPipeline.ACTION_ARCHIVE, null);
          pipeline.onRun(BasicPipeline.ACTION_UPLOAD, null);
    	}
    }
}
