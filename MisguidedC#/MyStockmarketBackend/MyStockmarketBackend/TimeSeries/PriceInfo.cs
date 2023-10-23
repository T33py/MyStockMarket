using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MyStockmarketBackend.TimeSeries
{
    /// <summary>
    /// Intraday series of prices for 100 timeslots.
    /// </summary>
    public class PriceInfo
    {
        int lastTime = -1;
        public int LastTimeslotUpdated { get => lastTime; }
        public bool ContainsInfo { get; set; } = false;

        public double[] Price { get; set; } = new double[100];
        public double CurrentPrice { get => Price[LastTimeslotUpdated]; }
        Random rand;

        public PriceInfo(Random rand)
        {
            this.rand = rand;
        }

        /// <summary>
        /// Update the priceinfo for a specific timeslot. 
        /// If the timeslot is in the future as compared to the last timeslot added, 
        /// then the timeslots inbetween will be interpolated.
        /// </summary>
        /// <param name="price"></param>
        /// <param name="time"></param>
        public void UpdatePriceinfo(int price, int time)
        {
            // if we skipped a timeslot interpolate the rest
            if (time - lastTime > 1)
            {
                for (int i = lastTime+1; i < time; i++)
                {
                    Price[i] = Interpolate(Price[lastTime], price, time - lastTime);
                }
            }
            Price[time] = price;
            lastTime = time;
            ContainsInfo = true;
        }

        /// <summary>
        /// Set the price of LastTimeslotUpdated+1.
        /// </summary>
        /// <param name="price">Prize to enter</param>
        public void UpdatePriceinfo(int price)
        {
            Price[++lastTime] = price;
            ContainsInfo = true;
        }

        double Interpolate(double from, double to, int dist, double fuzz = 0.02)
        {
            var dir = rand.Next(0, 1);
            if (dir == 0) { dir = -1; }
            return (to - from) * (1.0 / dist) * fuzz * dir;

        }
    }
}
