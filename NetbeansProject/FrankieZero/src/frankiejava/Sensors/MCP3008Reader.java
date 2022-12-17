/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package frankiejava.Sensors;

import com.pi4j.io.spi.SpiChannel;
import com.pi4j.io.spi.SpiDevice;
import com.pi4j.io.spi.SpiFactory;
import java.io.IOException;

/**
 *
 * @author simonjonsson
 */
public class MCP3008Reader {
    /**
     * Communicate to the ADC chip via SPI to get single-ended conversion value for a specified channel.
     * @param channel analog input channel on ADC chip
     * @return conversion value for specified analog input channel
     * @throws IOException
     */
    public static int getConversionValue(short channel) {

        // SPI device
        SpiDevice spi = null;
  
        // create a data buffer and initialize a conversion request payload
        byte data[] = new byte[] {
                (byte) 0b00000001,                              // first byte, start bit
                (byte)(0b10000000 |( ((channel & 7) << 4))),    // second byte transmitted -> (SGL/DIF = 1, D2=D1=D0=0)
                (byte) 0b00000000                               // third byte transmitted....don't care
        };

        
        try {
            spi = SpiFactory.getInstance(SpiChannel.CS0,
                SpiDevice.DEFAULT_SPI_SPEED, // default spi speed 1 MHz
                SpiDevice.DEFAULT_SPI_MODE);
            
            // send conversion request to ADC chip via SPI channel
            byte[] result2 = spi.write(data);
            // calculate and return conversion value from result bytes
            int value = (result2[1]<< 8) & 0b1100000000; //merge data[1] & data[2] to get 10-bit result
            value |=  (result2[2] & 0xff);
            return value;
        } catch (IOException e) {
            System.out.println("Simon - Something went wrong while reading MCP3008: " + e);
        }

        
       
        return 0;
    }
}
