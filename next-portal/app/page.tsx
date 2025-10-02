export default function Page() {
  const url = process.env.NEXT_PUBLIC_STREAMLIT_URL || 'http://localhost:8501'
  return (
    <main className="main">
      <div className="header">
        <div className="title">Urban Flood Risk Portal</div>
      </div>
      <div className="frameWrap">
        <iframe className="iframe" src={url} title="Streamlit Dashboard" />
      </div>
    </main>
  )
}
