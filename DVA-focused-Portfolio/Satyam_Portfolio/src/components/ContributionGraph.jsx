import { useState, useEffect } from "react"

export default function ContributionGraph() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const levels = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

  const levelMap = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4
  }

  useEffect(() => {
    fetch("https://github-contributions-api.deno.dev/SatyamKumarCS.json")
      .then(res => res.json())
      .then(res => {
        setData(res)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="contribution-section">
        <h3 className="contribution-title">Loading contributions...</h3>
      </div>
    )
  }

  if (!data || !data.contributions) return null

  const grid = data.contributions
  const total = data.totalContributions || 0

  return (
    <div className="contribution-section">
      <h3 className="contribution-title">
        {total.toLocaleString()} contributions in the last year
      </h3>
      <div className="contribution-graph">
        {grid.map((week, wi) => (
          <div key={wi} className="contribution-week">
            {week.map((day, di) => (
              <div
                key={di}
                className="contribution-cell"
                title={`${day.contributionCount} contributions on ${day.date}`}
                style={{ backgroundColor: levels[levelMap[day.contributionLevel] || 0] }}
              />
            ))}
          </div>
        ))}
      </div>
      <div className="contribution-legend">
        <span className="contribution-legend-label">Less</span>
        {levels.map((color, i) => (
          <div
            key={i}
            className="contribution-cell"
            style={{ backgroundColor: color }}
          />
        ))}
        <span className="contribution-legend-label">More</span>
      </div>
    </div>
  )
}
