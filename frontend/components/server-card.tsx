import React from 'react';
import { Server } from '@/lib/utils';

interface ServerCardProps {
  server: Server;
}

export function ServerCard({ server }: ServerCardProps) {
  return (
    <div className="flex flex-col p-6 bg-gray-800 shadow-md rounded-lg border border-gray-700 h-[200px] w-[300px]">
      <h3 className="text-lg font-semibold mb-2 text-blue-300">{server.name}</h3>
      <div className="flex flex-col gap-2 text-sm text-gray-300 flex-grow">
        <div className="flex justify-between">
          <span className="font-medium text-gray-400">ID:</span>
          <span className="truncate max-w-[180px]">{server.id}</span>
        </div>
        <div className="flex justify-between">
          <span className="font-medium text-gray-400">Loader:</span>
          <span>{server.loader}</span>
        </div>
        <div className="flex justify-between">
          <span className="font-medium text-gray-400">Game Version:</span>
          <span>{server.game_version}</span>
        </div>
      </div>
      <div className="flex justify-between mt-4">
        <button 
          className="px-3 py-1 bg-green-600 text-white rounded-md text-sm hover:bg-green-500 transition-colors"
          onClick={() => {
            fetch(`http://localhost:8000/servers/${server.id}/start`, {
              method: 'POST',
            });
          }}
        >
          Start
        </button>
        <button 
          className="px-3 py-1 bg-red-600 text-white rounded-md text-sm hover:bg-red-500 transition-colors"
          onClick={() => {
            fetch(`http://localhost:8000/servers/${server.id}/stop`, {
              method: 'PUT',
            });
          }}
        >
          Stop
        </button>
      </div>
    </div>
  );
}
