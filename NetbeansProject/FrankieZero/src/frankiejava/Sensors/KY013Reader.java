/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package frankiejava.Sensors;

/**
 *
 * @author simonjonsson
 */
public class KY013Reader {
    static short KY013Channel = 0;
    
    public static double getCelsius () {
        
        float R1 = 10000;
        //float R1 = 20000;
        double c1 = 0.001129148;
        double c2 = 0.000234125;
        double c3 = 0.0000000876741;
        
        int Vo = MCP3008Reader.getConversionValue(KY013Channel);
        double R2 = R1 * (1023.0 / (double)Vo - 1.0);
        double logR2 = Math.log(R2);
        double kelvin = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
        double celcius = kelvin - 273.15;
        
        return celcius;
    }
}
