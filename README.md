This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

![](https://github.com/YaredPena/Chatter-Box-AI-Chat-Support-August-2024/blob/main/public/gif/github.gif)

## Getting Started

First, run the frontend inside the app directory:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```
Then, run the development server inside the backend directory:
```bash
py app.py
```
Open [http://localhost:3000](http://localhost:3000) with your browser to see the frontend.
## Other Files
There are some helper python modules that were used in the creation of this project,
data_proc was used to clean the dataset and utilize only the helpful information available.
chroma_load was used to load the chromadb for our rag model to read from. It partitioned using a langchain csv loader and then used a openai embeddings model to store the data as vectors.


## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.
