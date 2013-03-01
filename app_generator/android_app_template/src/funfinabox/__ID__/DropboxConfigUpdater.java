package funfinabox.__ID__;

import android.content.Context;

import com.dropbox.client2.exception.DropboxException;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.JsonSyntaxException;

import edu.mit.media.funf.config.ConfigUpdater;

public class DropboxConfigUpdater extends ConfigUpdater {

  private Context context;
  
  @Override
  protected JsonObject getConfig() throws ConfigUpdateException {
    try {
      return new JsonParser().parse(DropboxUtil.getConfig(context)).getAsJsonObject();
    } catch (JsonSyntaxException e) {
      throw new ConfigUpdateException("Bad syntax in config", e);
    } catch (DropboxException e) {
      throw new ConfigUpdateException("Unable to contact dropbox", e);
    }
  }

}
