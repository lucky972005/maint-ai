# syntax=docker/dockerfile:1

# ------------------------------------------------------------------------------
# Stage 1: Base Image
# ------------------------------------------------------------------------------
FROM node:20-alpine AS base
WORKDIR /app
# Install libc6-compat for process compatibility on Alpine Linux
RUN apk add --no-cache libc6-compat

# ------------------------------------------------------------------------------
# Stage 2: Dependencies
# ------------------------------------------------------------------------------
FROM base AS deps
# Copy dependency manifests
COPY package.json package-lock.json ./
# Install production & development dependencies with frozen lockfile
RUN npm ci

# ------------------------------------------------------------------------------
# Stage 3: Builder
# ------------------------------------------------------------------------------
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Disable Next.js telemetry during build
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Provide build-time dummy fallback values for client-side environment vars so static generation succeeds
ENV NEXT_PUBLIC_SUPABASE_URL=https://placeholder-project.supabase.co
ENV NEXT_PUBLIC_SUPABASE_ANON_KEY=placeholder-anon-key

# Build Next.js application with standalone output
RUN npm run build

# ------------------------------------------------------------------------------
# Stage 4: Production Runner
# ------------------------------------------------------------------------------
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Create unprivileged system group and user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy static public assets
COPY --from=builder /app/public ./public

# Prepare .next directory with correct ownership
RUN mkdir .next && chown nextjs:nodejs .next

# Copy standalone build artifacts and client static assets
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to non-root user
USER nextjs

EXPOSE 3000

# Docker native container health check hitting the health route
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:3000/api/health || exit 1

# Start Next.js standalone server
CMD ["node", "server.js"]
