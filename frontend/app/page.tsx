'use client';

import React, { useState, useEffect } from 'react';
import { Plus } from 'lucide-react';
import { Server } from '@/lib/utils';
import { ServerCard } from '@/components/server-card';
import { CreateServerModal } from '@/components/create-server-modal';
import { Button } from '@/components/ui/button';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '@/components/ui/carousel';

export default function Home() {
  const [servers, setServers] = useState<Server[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  const fetchServers = async () => {
    try {
      setIsLoading(true);
      const response = await fetch('http://localhost:8000/servers/');
      
      if (!response.ok) {
        throw new Error('Failed to fetch servers');
      }
      
      const data = await response.json();
      setServers(data);
      setError(null);
    } catch (err) {
      setError('Failed to load servers. Please try again later.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchServers();
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center p-8 md:p-24">
      <h1 className="text-4xl font-bold mb-8 text-blue-400">Fourdrinier Server Manager</h1>
      
      <div className="w-full max-w-5xl mb-12">
        <h2 className="text-2xl font-semibold mb-4 text-blue-300">Your Servers</h2>
        
        {isLoading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        ) : error ? (
          <div className="bg-red-900 border border-red-700 text-red-100 px-4 py-3 rounded">
            {error}
          </div>
        ) : (
          <Carousel className="w-full">
            <CarouselContent>
              {servers.map((server) => (
                <CarouselItem key={server.id} className="md:basis-1/2 lg:basis-1/3">
                  <ServerCard server={server} />
                </CarouselItem>
              ))}
              <CarouselItem className="md:basis-1/2 lg:basis-1/3">
                <div className="flex items-center justify-center p-6 bg-gray-800 shadow-md rounded-lg border border-gray-700 h-[200px] w-[300px]">
                  <Button 
                    onClick={() => setIsCreateModalOpen(true)}
                    className="h-16 w-16 rounded-full bg-blue-600 hover:bg-blue-700"
                  >
                    <Plus className="h-8 w-8" />
                  </Button>
                </div>
              </CarouselItem>
            </CarouselContent>
            <div className="hidden md:flex">
              <CarouselPrevious className="left-0" />
              <CarouselNext className="right-0" />
            </div>
          </Carousel>
        )}
      </div>

      <CreateServerModal 
        open={isCreateModalOpen} 
        onOpenChange={setIsCreateModalOpen} 
        onServerCreated={fetchServers}
      />
    </main>
  );
}
