/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package frankiejava;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.lang.Math; 

/**
 *
 * @author simonjonsson
 */
public class LogFilesUtils {
    
    public static void appendToCSV (String filepath, String date, String temp, String pres) {
        String sep = ",";
        String row = "\n";
        
        ArrayList<String> data = readCSV(filepath);
        
        //System.out.println("The log file now contain:");
        //for (String line: data)
        //    System.out.println(line);
        
        //System.out.println("data.size()=" + data.size());
        if (data.size() < 1) {
            data.add("Date" + sep + "Temp" + sep + "Pres" + row);
            System.out.println("Added header");
        } 
        data.add(date + sep + temp + sep + pres + row);
        //System.out.println("data.size()=" + data.size());
        
        //System.out.println("We are now going to write:");
        //for (String line: data)
        //    System.out.println(line);
        
        writeCSV(filepath, data);
        
    }
    
    
    public static void writeCSV (String target, ArrayList<String> data) {
        
        try { 
            FileWriter csvWriter = new FileWriter(target);
            
            for (String row : data) {
                csvWriter.append(row);
            }

            csvWriter.flush();
            csvWriter.close();
            
        } catch (IOException e) {
            System.out.println("Simon - Something went wrong while writing csv file: " + e);
        }
    }
    
    public static ArrayList<String> readCSV(String filepath) {
        ArrayList<String> res = new ArrayList<>();
        File file = new File(filepath);
        String rowSep = "\n";
        
        if (!file.exists()) 
            return res;
        System.out.println("file.exists()=" + file.exists() + " (filepath=" + filepath + ")");
        
        BufferedReader br;
        try {
            br = new BufferedReader(new FileReader(file.getAbsolutePath()));
            String line;
            //System.out.println(br);
            //br.readLine();
            while ((line = br.readLine()) != null) {
                //System.out.println(line);
                try {
                    res.add(line + rowSep); 
                } catch (Exception e) {
                    System.out.println("Something went wrong: " + e);
                }  
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            /*if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }*/
        }
        //System.out.println("res.size()=" + res.size());
        return res;
    }
    
    //##########################################################################
    //##########################################################################
    //##########################################################################
    //##########################################################################
    //##########################      LEGACY     ###############################
    //##########################################################################
    //##########################################################################
    //##########################################################################
    //##########################################################################

    
    
    
 
    
    public static ArrayList<LogEntry> getLogEntries (String type, long startTimestamp, long endTimestamp) {
        
        Date startDateObj = new Date(startTimestamp);
        Date endDateObj = new Date(endTimestamp);
        
        //System.out.println("start=" + startDateObj.toString() + " end=" + endDateObj.toString());
        
        String startDateStr = new SimpleDateFormat("yyyy MM dd").format(startDateObj);
        String endDateStr = new SimpleDateFormat("yyyy MM dd").format(endDateObj);
        
        //System.out.println("start=" + startDateStr + " end=" + endDateStr);
        
        ArrayList<String> allDatesBetween = getAllDatesBetweenStr(startDateObj, endDateObj);
        
        final File logsFolder = new File("/home/pi/Logs");
        
        // filling files with the files that contains entries we are interested in.
        ArrayList<File> files = new ArrayList<File>();
        for (File file: logsFolder.listFiles()) {
            
            for (String date: allDatesBetween) {
                //System.out.println(file.getName());
                //String pattern = "^.*?\b" + date + "\b.*?\b" + type + "\b.*?\b" + "csv" +  "\b.*?$";
                String pattern = ".*" + date + ".*" + type + ".*" + ".csv";
                //System.out.println(pattern + "   date=" + date + "    type=" + type);
                if (file.getName().matches(pattern)) {
                    files.add(file);
                    //System.out.println("match!!! " + file);
                }
            }
        }
        
        
        ArrayList<LogEntry> res = new ArrayList<LogEntry>();
        
        for (File file: files) {
            BufferedReader br;
            try {
                br = new BufferedReader(new FileReader(file.getAbsolutePath()));
                String line;
                br.readLine();
                while ((line = br.readLine()) != null) {
                    try {
                        //System.out.println("getLogEntries: " + line);
                        String[] splitLine = line.split(",");
                        if (splitLine.length > 2) {
                            String firstPart = splitLine[0].trim();
                            Date datetime = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").parse(firstPart + " " + splitLine[1]);
                            if (datetime.getTime() > startTimestamp & datetime.getTime() < endTimestamp) {
                                res.add(new LogEntry(type, line));
                            }
                        }
                    } catch (ParseException e) {
                        System.out.println("Something went wrong: " + e);
                    }  

                }
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                /*if (br != null) {
                    try {
                        br.close();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }*/
            }
        }
        
        Collections.sort(res);
        return res;
    }
    
    public static ArrayList<String> getAllDatesBetweenStr (Date startObj, Date endObj) {
        ArrayList<String> res = new ArrayList<String>();
        
        LocalDate ld = startObj.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
        LocalDate start = LocalDate.of(ld.getYear(), ld.getMonthValue(), ld.getDayOfMonth());
        
        ld = endObj.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
        LocalDate end = LocalDate.of(ld.getYear(), ld.getMonthValue(), ld.getDayOfMonth());
        
        while (!start.isAfter(end)) {
            res.add(new SimpleDateFormat("yyyy MM dd").format(Date.from(start.atStartOfDay().atZone(ZoneId.systemDefault()).toInstant())));
            start = start.plusDays(1);
        }
        return res;
    }
    
    
    
    public static void printMinTempPerDay () {
        ArrayList<String> dates = new ArrayList<>();
        try {
            dates = getAllDatesBetweenStr(new SimpleDateFormat("yyyy MM dd").parse("2016 08 08"), new Date());
        } catch (ParseException e) {
            System.out.println(e);
        }
        
        for (int i = 0; i < dates.size(); i++) {
            String date = dates.get(i);
            //System.out.println(date);
            long startTimestamp = 0L;
            long stopTimestamp = 0L;
            try {
                Date startDate = new SimpleDateFormat("yyyy MM dd hh:mm").parse(date + " 00:00");
                Date stopDate = new SimpleDateFormat("yyyy MM dd hh:mm").parse(date + " 04:00");
                startTimestamp = startDate.getTime();
                stopTimestamp = stopDate.getTime();
            } catch (ParseException e) {
                System.out.println("Whoa, something went wrong!" + e);
            }
            
            ArrayList<LogEntry> entries = getLogEntries(LogEntry.TEMP_HUM, startTimestamp, stopTimestamp);
            
            if (entries.size() > 0) {
                double sumTemp = 0;
                int countTemp = 0;
                double min = 1000;
                double max = 0;
                for (int i2 = 0; i2 < entries.size(); i2++) {
                    LogEntry entry = entries.get(i2);
                    double temp = entry.getValue1Dbl();
                    sumTemp += temp;
                    countTemp++;
                    if (temp < min) min = temp;
                    if (temp > max) max = temp;
                    //System.out.println(entry.dateStr + "\t" + entry.timeStr + "\t" + entry.value1Str);
                }
                double mean = sumTemp / (double) countTemp;
                System.out.println(date + "\t" + String.valueOf(Math.round(mean)) + "\t" + String.valueOf(Math.round(min)) + "\t" + String.valueOf(Math.round(max)) );
            }
            
            //System.out.println("date=" + date + "\tstartTimestamp=" + startTimestamp + "\tstopTimestamp=" + stopTimestamp);
            
        }
    }
    
    
}
