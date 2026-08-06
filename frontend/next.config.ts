import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Tauri carica il frontend come file statici (protocollo tauri://),
  // senza un server Node: serve l'export statico di Next.
  output: "export",
  images: {
    // next/image richiede un server per l'ottimizzazione: disattivata
    // per l'export statico. Le immagini arrivano comunque dal backend
    // FastAPI su http://127.0.0.1:8000/static/... senza bisogno di proxy.
    unoptimized: true,
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8000',
        pathname: '/**',
      },
      {
        protocol: 'http',
        hostname: '127.0.0.1',
        port: '8000',
        pathname: '/**',
      },
    ],
  },
};

export default nextConfig;