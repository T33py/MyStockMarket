using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MyStockmarketBackend.WorldInfo
{
    public class Indexes
    {
        /// <summary>
        /// Index of the 1000 biggest companies by revenue
        /// </summary>
        public Company[] Global1000Index = new Company[1000];
        bool global1000Generated = false;

        public List<Company> GenerateIndex(List<Company> companies, Type type)
        {
            var index = new List<Company>();

            switch (type)
            {
                case Type.Global:
                    if (!global1000Generated)
                        GenerateGlobal1000(companies);
                    index.AddRange(Global1000Index);
                    break;
                default:break;
            }

            return index;
        }

        /// <summary>
        /// Go through provided companies to pick out the 1000 with the highest revenue
        /// </summary>
        /// <param name="companies"></param>
        void GenerateGlobal1000(List<Company> companies) 
        {
            var revIndex = new Dictionary<int, int>();
            int minRev = 0;
            int idx = 0;
            foreach (var company in companies)
            {
                var kv = company.Stock.LatestKeyvalues;
                int rev = kv is null ? 0 : kv.Revenue;
                if (rev == 0) { }
                else if (idx < 1000)
                {
                    Global1000Index[idx] = company;
                    revIndex[rev] = idx;
                    idx++;
                }
                else if (rev > minRev)
                {
                    idx = revIndex[minRev];
                    revIndex.Remove(minRev);
                    Global1000Index[idx] = company;
                    revIndex[rev] = idx;
                    minRev = revIndex.Keys.Min();
                }
            }
            global1000Generated = true;
        }


        public enum Type
        {
            Global,
            GlobalLimited,
            CountryLargeCap,
            CountryMidCap,
            CountrySmallCap,
            Sector,
        }
    }
}
