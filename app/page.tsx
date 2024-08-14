'use client'

import Head from 'next/head';
import Chat from './components/Chat';

export default function Home() {
  return (
    <div>
      <main className="flex flex-col items-center justify-center min-h-screen p-4">
        <h1 className="text-4xl font-bold mb-8">Welcome to Chatterbox</h1>
        <Chat />
      </main>
    </div>
  );
}
