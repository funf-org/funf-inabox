/**
 * 
 * Funf: Open Sensing Framework
 * Copyright (C) 2010-2011 Nadav Aharony, Wei Pan, Alex Pentland.
 * Acknowledgments: Alan Gardner
 * Contact: nadav@media.mit.edu
 * 
 * Author(s): Swetank Kumar Saha (swetank.saha@gmail.com)
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
package edu.mit.media.funf.probe.external;


import android.app.Activity;
import android.content.ComponentName;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.view.ViewGroup.LayoutParams;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.LinearLayout;

import com.google.gson.JsonObject;

import edu.mit.media.funf.FunfManager;
import edu.mit.media.funf.json.IJsonObject;
import edu.mit.media.funf.json.JsonUtils;
import edu.mit.media.funf.pipeline.BasicPipeline;
import edu.mit.media.funf.pipeline.Pipeline;
import edu.mit.media.funf.time.TimeUtil;

public class WebViewActivity extends Activity{
	
	public static final String PIPELINE_NAME = "__NAME__";
	
	private static String URL; //The URL that WebView will render
	
	private FunfManager funfMgr = null;
	private Pipeline pipeline = null;
	private ServiceConnection funfMgrConn = new ServiceConnection() {
	      
	    @Override
	    public void onServiceConnected(ComponentName name, IBinder service) {
	      funfMgr = ((FunfManager.LocalBinder)service).getManager();
	      pipeline = funfMgr.getRegisteredPipeline(PIPELINE_NAME);
	      
	      JsonObject config = new JsonObject();
	      config.addProperty("@type", "edu.mit.media.funf.probe.external.UserStudyNotificationProbe");
	      JsonObject data = new JsonObject();
	      data.addProperty("timestamp", TimeUtil.getTimestamp());
	      data.addProperty("webviewUrl", URL);
		  data.addProperty("type", "notification_open");
		  
		  BasicPipeline basicPipeline = (BasicPipeline) pipeline;
	      basicPipeline.onDataReceived((IJsonObject)JsonUtils.immutable(config), (IJsonObject)JsonUtils.immutable(data));
	    }

		@Override
		public void onServiceDisconnected(ComponentName name) {
			funfMgr = null;
		}
	};
	
	@Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
		LinearLayout view = new LinearLayout(getApplicationContext());
		view.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT));
		view.setOrientation(LinearLayout.VERTICAL);

		WebView web = new WebView(this);
		//Button b = new Button(this);
		web.setLayoutParams(new LayoutParams(
				LayoutParams.MATCH_PARENT,
				LayoutParams.WRAP_CONTENT));
		web.getSettings().setJavaScriptEnabled(true);
		web.setWebViewClient(new WebViewClient());
		
		URL = getIntent().getStringExtra("url");
		web.loadUrl(URL);
		
		view.addView(web);
		setContentView(view);
		
		bindService(new Intent(this, FunfManager.class), funfMgrConn, BIND_AUTO_CREATE);
	}
	
}
