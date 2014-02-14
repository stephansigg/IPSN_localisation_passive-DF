package deviceFree.rssimonitor;

import java.io.DataOutputStream;
import java.io.IOException;
import java.util.ArrayList;

import eu.chainfire.libsuperuser.Shell;
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
	
//	public void startSetup(View view){
//		// sh /sdcard/setup.sh
//	    Process p; 
//	    try {   
//	       // Preform su to get root privledges  
//	       p = Runtime.getRuntime().exec("su");   
//	       DataOutputStream os = new DataOutputStream(p.getOutputStream());   
//	       os.writeBytes("sh /sdcard/setup.sh > /sdcard/setupOutput.txt\n");
//	       os.flush();
//	       os.close();
//	       //os.writeBytes("sh /sdcard/setup.sh\n")
//	       p.waitFor();
//	    } catch (IOException e) {   
//	       // TODO Code to run in input/output exception  
//	        //toastMessage("not root");   
//	    } catch (InterruptedException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
//	    
//	    Process p2;
//	    try{
//	       p2 = Runtime.getRuntime().exec("su");
//	       DataOutputStream os2 = new DataOutputStream(p2.getOutputStream());   
//	       os2.writeBytes("tcpdump eth0 -w /sdcard/myTestOutput140207.cap\n");
//	       os2.flush();
//	       os2.close();
//		} catch (IOException e) {   
//	       // TODO Code to run in input/output exception  
//	        //toastMessage("not root");   
//	    }
//	    
//		Process pSetup;
//		try {
//			pSetup = Runtime.getRuntime().exec("sh /sdcard/setup.sh");
//		}catch (IOException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//			}
//		//BufferedReader in = new BufferedReader(new InputStreamReader(pSetup.getInputStream()));
//	}
	
	public void startSetup(View view){
		Thread th = new Thread(new Runnable() {
			
			@Override
			public void run() {
				ArrayList<String> liste = new ArrayList<String>();
				liste.add("sh /sdcard/setup.sh");
				//liste.add("cd /sdcard/");
				//liste.add("mkdir neuerOrdner");
				liste.add("sleep 10");
				//liste.add("tcpdump eth0 -w /sdcard/myTestOutput140207.cap");
				//liste.add("sh /sdcard/startTcpdump.sh &");
				liste.add("tcpdump -w /sdcard/myTestOutput140208.cap");
				//liste.add("ls > /sdcard/nochEinOutput.txt");
				liste.add("sleep 20");
				//liste.add("mv /sdcard/myTestOutput140208 /sdcard/myTestOutput_sample");
				//liste.add("tcpdump -w /sdcard/myTestOutput140209.cap");
				// sh /sdcard/setup.sh
				//liste.add("killall tcpdump");
				Shell.SU.run(liste);
//			       Shell.SU.run("sh /sdcard/setup.sh > /sdcard/setupOutput.txt\n");
//			       Shell.SU.run("tcpdump eth0 -w /sdcard/myTestOutput140207.cap\n");				
			}
		});
		th.start();
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
	