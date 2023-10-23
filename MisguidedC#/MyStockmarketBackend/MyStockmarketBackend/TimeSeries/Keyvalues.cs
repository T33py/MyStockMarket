using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MyStockmarketBackend.TimeSeries
{
    public class Keyvalues
    {
        public int Year { get; set; }
        public int Revenue {  get; set; }
        public int CostOfRevenue { get; set; }


        public int SharesOutstanding { get; set; }
        public int CashAndEquivalents { get; set; }
        public int InterestBearingDebt { get; set; }
        public int NonInterestBearingDebt { get; set; }
    }
}
