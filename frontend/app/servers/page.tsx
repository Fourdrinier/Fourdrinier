import React from 'react'

interface Server {
    id: string
    name: string
}

const ServersPage = async () => {
    const res = await fetch('http://backend:8000/servers/')
    const servers: Server[] = await res.json()

    return (
        <div className='min-h-screen min-w-screen bg-neutral-800'>
            <h1 className='bg-slate-700 text-black'>Servers</h1>
            <ul>
                {servers.map((server) => (
                    <li key={server.id}>
                        <a href={`/servers/${server.id}`}>{server.name}</a>
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default ServersPage