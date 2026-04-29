const base = import.meta.env.BASE_URL

const projects = [
  {
    name: "British Airways Analytics",
    description: "Analyzing passenger reviews and feedback to uncover actionable insights for improving service quality and customer satisfaction.",
    image: `${base}airway.png`,
    tags: ["Tableau", "Data Analytics"],
    github: "https://github.com/SatyamKumarCS/British_Airway_Analytics",
    live: "https://public.tableau.com/views/BritishAirwaysReviews_17771972241220/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
  },
  {
    name: "Credit Card Complaints Analysis",
    description: "A comprehensive dashboard for analyzing credit card complaints, highlighting common issues and resolution efficiency.",
    image: `${base}credit_card.png`,
    tags: ["Tableau", "Data Analytics"],
    github: "https://github.com/SatyamKumarCS/CC_Analytics",
    live: "https://public.tableau.com/views/CreditCardComplaintsAnalysis_17773547265660/MainDashboard?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
  },
  {
    name: "Covid-19 Analytics",
    description: "Interactive dashboard visualizing Covid-19 data across India, tracking case trends, recoveries, and state-wise impacts.",
    image: `${base}Covid19.png`,
    tags: ["Tableau", "Python", "Data Analytics"],
    github: "https://github.com/SatyamKumarCS/Covid-19_Analytics",
    live: "https://public.tableau.com/views/Covid-19_India_Dashboard_17772026273670/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
  },
  {
    name: "Road Accident Analytics",
    description: "Detailed analysis of road accidents to identify patterns, causes, and areas for potential safety improvements.",
    image: `${base}accident.png`,
    tags: ["Tableau", "Data Analytics"],
    github: "https://github.com/SatyamKumarCS/Accident_Analytics",
    live: "https://public.tableau.com/app/profile/satyam.kumar1528/viz/Road_Accident_Analysis_17772104587190/RoadAccident_Dashboard"
  },
  {
    name: "Amazon PrimeVideo Analytics",
    description: "An exploratory data analysis of the Amazon Prime Video catalog, examining content distribution, ratings, and genres.",
    image: `${base}primevideo.png`,
    tags: ["Tableau", "Python", "Data Analytics"],
    github: "https://github.com/SatyamKumarCS/Amazon_PrimeVideo",
    live: "https://public.tableau.com/views/Primevideo_Dashboard_17772113602890/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
  },
  {
    name: "Real Estate Market Analysis",
    description: "A comprehensive Excel-based real estate market analysis and investment strategy evaluating property trends and profitability.",
    image: `${base}real_estate.png`,
    tags: ["Excel", "Data Analytics"],
    github: "https://github.com/SatyamKumarCS/SectionA_Group8",
    live: "https://docs.google.com/spreadsheets/d/1QU5AEmZaSJcBjNW9MoLuTMz_-Acxpx7rbuLUTRQnjZs/edit?usp=sharing"
  },
]

export default projects
