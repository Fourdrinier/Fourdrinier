import React from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { ServerCreate } from '@/lib/utils';
import { useToast } from '@/components/ui/use-toast';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

const formSchema = z.object({
  name: z.string().min(1, 'Server name is required'),
  loader: z.string().min(1, 'Loader is required'),
  game_version: z.string().regex(/^\d+\.\d+\.\d+$/, 'Game version must be in format X.Y.Z'),
});

interface CreateServerModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onServerCreated: () => void;
}

export function CreateServerModal({ open, onOpenChange, onServerCreated }: CreateServerModalProps) {
  const { toast } = useToast();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ServerCreate>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: 'My Server',
      loader: 'paper',
      game_version: '',
    },
  });

  const onSubmit = async (data: ServerCreate) => {
    try {
      const response = await fetch('http://localhost:8000/servers/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Failed to create server');
      }

      const result = await response.json();
      toast({
        title: 'Server Created',
        description: `Server "${data.name}" has been created successfully.`,
      });
      
      reset();
      onOpenChange(false);
      onServerCreated();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to create server. Please try again.',
        variant: 'destructive',
      });
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px] bg-gray-800 border-gray-700 text-gray-100">
        <DialogHeader>
          <DialogTitle className="text-blue-300">Create New Server</DialogTitle>
          <DialogDescription className="text-gray-400">
            Fill in the details to create a new Minecraft server.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="name" className="text-right text-gray-300">
                Name
              </Label>
              <div className="col-span-3">
                <Input id="name" {...register('name')} className="bg-gray-700 border-gray-600 text-gray-100" />
                {errors.name && (
                  <p className="text-sm text-red-400 mt-1">{errors.name.message}</p>
                )}
              </div>
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="loader" className="text-right text-gray-300">
                Loader
              </Label>
              <div className="col-span-3">
                <Input id="loader" {...register('loader')} className="bg-gray-700 border-gray-600 text-gray-100" />
                {errors.loader && (
                  <p className="text-sm text-red-400 mt-1">{errors.loader.message}</p>
                )}
              </div>
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="game_version" className="text-right text-gray-300">
                Game Version
              </Label>
              <div className="col-span-3">
                <Input 
                  id="game_version" 
                  placeholder="1.17.1" 
                  {...register('game_version')} 
                  className="bg-gray-700 border-gray-600 text-gray-100 placeholder:text-gray-500"
                />
                {errors.game_version && (
                  <p className="text-sm text-red-400 mt-1">{errors.game_version.message}</p>
                )}
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button type="submit" disabled={isSubmitting} className="bg-blue-600 hover:bg-blue-700 text-white">
              {isSubmitting ? 'Creating...' : 'Create Server'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
