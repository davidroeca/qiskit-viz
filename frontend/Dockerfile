#####################################################################
# Base stage
#####################################################################
FROM node:24-alpine3.22 AS base

ARG USERID=1001

# Modify the node user to use the provided USERID
RUN deluser --remove-home node \
    && addgroup -g ${USERID} node \
    && adduser -D -u ${USERID} -G node node

RUN mkdir -p /home/node/src && chown node:node /home/node/src

WORKDIR /home/node/src

COPY --chown=node:node package.json package-lock.json ./

FROM base AS deps
USER node
RUN npm ci

#####################################################################
# Build stage
#####################################################################
FROM base AS build
USER root
COPY --from=deps --chown=node:node /home/node/src/node_modules ./node_modules
COPY --chown=node:node . .

USER node
WORKDIR /home/node/src
RUN npm run build

#####################################################################
# Development stage
#####################################################################
FROM base AS development
USER root

COPY --from=deps --chown=node:node /home/node/src/node_modules ./node_modules
COPY --chown=node:node . .

USER node
WORKDIR /home/node/src
EXPOSE 5173
ENV NODE_ENV=development
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

FROM base AS production
USER root

#####################################################################
# Copy production dependencies
#####################################################################
COPY --from=deps --chown=node:node /home/node/src/node_modules ./node_modules
# Copy built application
COPY --from=build --chown=node:node /home/node/src/build ./build
# Copy package.json for metadata
COPY --chown=node:node package.json ./

USER node
WORKDIR /home/node/src
EXPOSE 3000
ENV NODE_ENV=production
CMD ["node", "build"]
