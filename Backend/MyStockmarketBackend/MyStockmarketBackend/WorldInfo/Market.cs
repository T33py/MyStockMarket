using MyStockmarketBackend.Concepts;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MyStockmarketBackend.WorldInfo
{
    public class Market
    {
        public Directions Direction { get; set; } = Directions.Neutral;
        public Directions DirectionGoingTowards { get; set; } = Directions.Neutral;
        public Moods Mood { get; set; } = Moods.Neutral;
        public Moods MoodGoingTowards { get; set;} = Moods.Neutral;
        public List<Company> Companies { get; set; } = new List<Company>();
        public List<Fund> Funds { get; set; } = new List<Fund>();
        public List<Bond> Bonds { get; set; } = new List<Bond>();
        public Indexes Indexes { get; set; } = new Indexes();
    }
}
