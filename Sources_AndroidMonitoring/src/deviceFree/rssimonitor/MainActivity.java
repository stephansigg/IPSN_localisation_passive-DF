package deviceFree.rssimonitor;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.view.View;

public class MainActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}
	
	public void startSetup(View view){
		// sh /sdcard/setup.sh
	    Process p;   
	    try {   
	       // Preform su to get root privledges  
	       p = Runtime.getRuntime().exec("su");   
	       DataOutputStream os = new DataOutputStream(p.getOutputStream());   
	       //os.writeBytes("ls > /sdcard/myLs.txt\n");
	       // Why can I write this ls function and also then write further commands with other output streams but not do this without the initial ls output stream?
	       //os.flush();
	       //DataOutputStream os2 = new DataOutputStream(p.getOutputStream());	
	       //os2.writeBytes("sh /sdcard/setup.sh\n");
	       //os2.writeBytes("tcpdump -w /sdcard/myTestOutput2.txt\n");
	       //os2.flush();
	       //p = Runtime.getRuntime().exec("su");
	       //os.close();
	       //DataOutputStream os = new DataOutputStream(p.getOutputStream());   
	       os.writeBytes("cd /sdcard  && setup.sh && tcpdump eth0 -w myTestOutputNeu.txt\n");
	       os.flush();
	       // Attempt to write a file to a root-only   
	       /** DataOutputStream os = new DataOutputStream(p.getOutputStream());   
	       os.writeBytes("echo \"Do I have root?\" >/system/sd/temporary.txt\n");  
	         
	       // Close the terminal  
	       os.writeBytes("exit\n");   
	       os.flush();   
	       try {   
	          p.waitFor();   
	               if (p.exitValue() != 255) {   
	                  // TODO Code to run on success  
	                  //toastMessage("root");  
	               }   
	               else {   
	                   // TODO Code to run on unsuccessful  
	                   //toastMessage("not root");      
	               }   
	       } catch (InterruptedException e) {   
	          // TODO Code to run in interrupted exception  
	          // toastMessage("not root");   
	       }   **/
	    } catch (IOException e) {   
	       // TODO Code to run in input/output exception  
	        //toastMessage("not root");   
	    } 
		
		Process pSetup;
		try {
			pSetup = Runtime.getRuntime().exec("sh /sdcard/setup.sh");
		}catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			}
		//BufferedReader in = new BufferedReader(new InputStreamReader(pSetup.getInputStream()));
	}
	
	public void startTcpdump(View view){
		// sh /sdcard/setup.sh
	    Process p2;   
	    try {   
	       // Preform su to get root privledges  
	       p2 = Runtime.getRuntime().exec("su");   
	         
	       // Attempt to write a file to a root-only   
	    } catch (IOException e) {   
	       // TODO Code to run in input/output exception  
	        //toastMessage("not root");   
	    } 
		
		Process pTcpdump;
		try {
			pTcpdump = Runtime.getRuntime().exec("tcpdump -w /sdcard/myTestOutput4.txt");
			DataOutputStream os = new DataOutputStream(pTcpdump.getOutputStream());   
		    os.writeBytes("tcpdump -w /sdcard/myTestOutput3.txt");
		}catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			}
		//BufferedReader in = new BufferedReader(new InputStreamReader(pSetup.getInputStream()));
	}
	
}
	