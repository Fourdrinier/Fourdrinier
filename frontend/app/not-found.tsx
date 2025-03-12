'use client';

import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 text-center">
      <h1 className="text-4xl font-bold mb-4 text-blue-400">404 - Page Not Found</h1>
      <p className="mb-8 text-gray-400">The page you are looking for does not exist.</p>
      <Link href="/" className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-500 transition-colors">
        Return to Home
      </Link>
    </div>
  );
}
