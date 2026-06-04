import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Pin the Turbopack workspace root to this src/ directory.
  // The repo is a hybrid: Python (uv) at the repo root, Node only in src/.
  // Without this, a stray package-lock.json at the repo root makes Turbopack
  // infer the wrong workspace root and fail to resolve node_modules (e.g.
  // "Cannot find module 'lucide-react'").
  turbopack: {
    root: __dirname,
  },
};

export default nextConfig;
