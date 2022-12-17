/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package frankiejava;

import frankiejava.Sensors.DHT11Reader;
import frankiejava.Sensors.KY013Reader;
import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;

/**
 *
 * @author simonjonsson
 */
public class FrankieZero {

    final static String LOG_FILE_PATH = "/home/pi/Desktop/logs.csv";
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws InterruptedException {

        //double c = KY013Reader.getCelsius();
        //System.out.println("KY013Reader.getCelsius()=" + c);
        //mcpTimer(1000*2);
        
        readingsTimer(1000*60*10);
        
        System.out.println("Done!!");
    }
    
    public static void readingsTimer (int interval) {
        Timer timer = new Timer();
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                
                frankiejava.Sensors.BMP280Reader reader = new frankiejava.Sensors.BMP280Reader();
                LogFilesUtils.appendToCSV(LOG_FILE_PATH, reader.getDate(), reader.getTemp(), reader.getPres());
             
                double c = KY013Reader.getCelsius();
                System.out.println("KY013Reader.getCelsius()=" + c + "     BMP280-Date=" + reader.getDate() + "     -Temp=" + reader.getTemp().toString() + "     -Pres=" + reader.getPres().toString());
            }
        }, 0, interval);
    }
    
    public static void mcpTimer (int interval) {
        Timer timer = new Timer();
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                
                double c = KY013Reader.getCelsius();
                System.out.println("KY013Reader.getCelsius()=" + c);
             
            }
        }, 0, interval);
    }
    
}
