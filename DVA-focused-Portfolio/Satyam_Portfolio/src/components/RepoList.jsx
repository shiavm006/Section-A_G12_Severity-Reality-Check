import RepoCard from "./RepoCard"

export default function RepoList({projects,activeFilter,setActiveFilter,onCardClick}){
  const allTags=["All",...new Set(projects.flatMap((p)=>p.tags))]
  const filtered=activeFilter==="All"
    ? projects
    : projects.filter((p)=>p.tags.includes(activeFilter))

  return(
    <div className="repo-list">
      <div className="repo-list-header">
        <svg viewBox="0 0 16 16" width="16" height="16" fill="#8b949e">
          <path d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5zm10.5-1h-8a1 1 0 00-1 1v6.708A2.486 2.486 0 014.5 9h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"/>
        </svg>
        <span className="repo-list-title">Repositories</span>
        <span className="repo-list-count">{filtered.length}</span>
      </div>

      <div className="repo-list-filters">
        {allTags.map((tag)=>(
          <button
            key={tag}
            className={"filter-tab"+(activeFilter===tag?" filter-tab-active":"")}
            onClick={()=>setActiveFilter(tag)}
          >
            {tag}
          </button>
        ))}
      </div>

      <div className="repo-grid">
        {filtered.map((project)=>(
          <RepoCard
            key={project.name}
            project={project}
            onClick={onCardClick}
          />
        ))}
      </div>
    </div>
  )
}
