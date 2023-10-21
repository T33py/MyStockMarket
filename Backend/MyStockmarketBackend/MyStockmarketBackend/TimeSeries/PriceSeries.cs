using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MyStockmarketBackend.TimeSeries
{
    public class PriceSeries
    {
        Random rand;
        public int Weekday { get; set; }

        /// <summary>
        /// The priceinfo for the current trading day.
        /// </summary>
        public PriceInfo Intraday { get; set; }

        /// <summary>
        /// The current tradingweek.
        /// </summary>
        public PriceWeek CurrentWeek { get => CurrentYear.LastWeek; }

        /// <summary>
        /// The current trading year.
        /// </summary>
        public PriceYear CurrentYear { get; set; }

        /// <summary>
        /// Historic data for the stock.
        /// </summary>
        public List<PriceYear> HistoricData { get; set; } = new List<PriceYear>();

        public PriceSeries(Random rand) 
        { 
            this.rand = rand;
            Intraday = new PriceInfo(rand);
        }

        public void AdvanceDay()
        {
            Weekday = (Weekday + 1) % 5;
            if (Weekday == 0) 
            { 
                if (CurrentYear.Weeks >= 52)
                {
                    CurrentYear = new PriceYear(rand);
                    HistoricData.Add(CurrentYear);
                }
                CurrentYear.NewWeek();
            }
            Intraday = CurrentWeek.DayByNumber(Weekday);
        }
    }

    public class PriceYear
    {
        Random rand;

        /// <summary>
        /// The year for which this is info.
        /// </summary>
        public int Year { get; set; }
        /// <summary>
        /// Number of weeks this contains info on.
        /// </summary>
        public int Weeks { get => WeeklyInfo.Count; }
        /// <summary>
        /// The final week in this year (current week if current year).
        /// </summary>
        public PriceWeek LastWeek {  get; set; }
        /// <summary>
        /// All weeks in the year.
        /// </summary>
        List<PriceWeek> WeeklyInfo { get; } = new List<PriceWeek>();

        public PriceYear(Random rand)
        {
            this.rand = rand;
        }

        /// <summary>
        /// Generate a new week in this year.
        /// </summary>
        public void NewWeek()
        {
            if (LastWeek is null)
            {
                LastWeek = new PriceWeek(rand) { Week = 1 };
            }
            else
            {
                LastWeek = new PriceWeek(rand) { Week = LastWeek.Week + 1 };
            }
            WeeklyInfo.Add(LastWeek);
        }
    }

    public class PriceWeek
    {
        Random rand;
        public int Week { get; set; }
        public PriceInfo Monday { get; set; }
        public PriceInfo Tuesday { get; set; }
        public PriceInfo Wednesday { get; set; }
        public PriceInfo Thursday { get; set; }
        public PriceInfo Friday { get; set; }

        public PriceInfo[] Days { get => new PriceInfo[] { Monday, Tuesday, Wednesday, Thursday, Friday }; }

        public PriceWeek(Random rand)
        {
            this.rand = rand;
            Monday = new PriceInfo(rand);
            Tuesday = new PriceInfo(rand);
            Wednesday = new PriceInfo(rand);
            Thursday = new PriceInfo(rand);
            Friday = new PriceInfo(rand);
        }


        /// <summary>
        /// Get 0 based day of the week. Monday is considered day 0.
        /// </summary>
        /// <param name="day">Number of the day</param>
        /// <returns>Day requested.</returns>
        public PriceInfo DayByNumber (int day)
        {
            switch (day)
            {
                case 0: return Monday;
                case 1: return Tuesday;
                case 2: return Wednesday;
                case 3: return Thursday;
                case 4: return Friday;
                default: return Friday;
            }
        }
    }
}
