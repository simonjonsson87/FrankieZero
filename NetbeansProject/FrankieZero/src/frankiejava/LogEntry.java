/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package frankiejava;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 *
 * @author simonjonsson
 */
public class LogEntry implements Comparable {
    
    public static final String CO2 = "CO2";
    public static final String TEMP_HUM = "TempHum";
    public static final String TEMP_PRES = "TempPress";
    public static final String RGB = "RGB";
    
    String type, dateStr, timeStr, value1Str, value2Str;
    String value1StrShort, value2StrShort, value1Str1dec, value2Str1dec;
    Date date;
    double value1Dbl, value2Dbl;
    long timestamp;
   
    public LogEntry (String type, String row) {
        this.type = type;
        row = row.trim();
        String[] splitRow = row.split(",");
        this.dateStr = splitRow[0];
        this.timeStr = splitRow[1];
        this.value1Str = splitRow[2];
        if (splitRow.length > 3) { 
            this.value2Str = splitRow[3];
            if (value2Str.contains(".")) this.value2StrShort = value2Str.split("\\.")[0];
            this.value2Str1dec = String.valueOf(Math.round(Double.parseDouble(value2Str) * 10) / 10.0);
        }
        
        if (value1Str.contains(".")) {
            this.value1StrShort = value1Str.split("\\.")[0];
        } else {
            this.value1StrShort = value1Str;
        }
        this.value1Str1dec = String.valueOf(Math.round(Double.parseDouble(value1Str) * 10) / 10.0);

        String fullDateStr = dateStr + timeStr;
        try {
            date = new SimpleDateFormat("yyyy-MM-ddHH:mm:ss").parse(fullDateStr);
        } catch (ParseException e) {
            System.out.println("Something went wrong while parsing date: " + e);
        }
        
        timestamp = date.getTime();
    }
    
    public long getTimestamp () { return timestamp; }
    
    public double getValue1Dbl () { return Double.parseDouble(value1Str); }
    public double getValue2Dbl () { return Double.parseDouble(value2Str); }
    
    public int getValue1Int () { return Integer.parseInt(value1Str); }
    public int getValue2Int () { return Integer.parseInt(value2Str); }
    
    @Override
    public int compareTo (Object o) {
        long jan2019ms = 1546300800000L;
        int thisreducedtimestamp = (int) (this.timestamp - jan2019ms);
        int compareTimestamp = (int) ( ((LogEntry)o).timestamp-jan2019ms );
       
        return thisreducedtimestamp-compareTimestamp;
    }

}
