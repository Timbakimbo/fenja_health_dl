# Fenja Health Frontend

React 19 + TypeScript + Vite frontend for the Fenja health tracker.

## Local development

```bash
cp .env.example .env
npm install
npm run dev
```

`npm run dev` starts Vite with `--host`, so the app is reachable from other devices on your local network.

## Environment

```bash
VITE_API_URL=http://localhost:8000
VITE_API_KEY=your-secret-api-key-here
```

For phone or tunnel testing, point `VITE_API_URL` at the backend origin the device can actually reach.

## PWA / mobile install

- The app uses `vite-plugin-pwa`
- The manifest and service worker are generated during `npm run build`
- Built assets are precached automatically

For a real installable PWA on a phone, serve the app from a secure origin (`https://...`) or test on `localhost` on the same device.

## Production preview

```bash
npm run build
npm run preview
```
