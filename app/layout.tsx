import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Chatterbox",
  description: "An AI Chat Support bot",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="bg-black">
      <body className={`${inter.className} flex justify-center items-center min-h-screen bg-black`}>
        <div className="flex flex-row items-center">
          {/* GIF Container */}
          <div className="flex-shrink-0 mr-8">
            <img src="/gif/falco-starfox.gif" alt="Falco Starfox" className="w-44 h-auto" />
          </div>
          {/* Chatbox Container */}
          <div className="flex-1">
            {children}
          </div>
        </div>
      </body>
    </html>
  );
}
