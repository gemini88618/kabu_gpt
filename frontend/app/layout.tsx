import type { Metadata, Viewport } from "next";
import "./globals.css";
import { ServiceWorkerRegister } from "@/components/service-worker-register";

export const metadata: Metadata = {
  title: "Stock Scanner",
  description: "Japan and US stock screening PWA",
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    title: "Stocks",
    statusBarStyle: "black-translucent"
  },
  icons: {
    apple: "/icon.png",
    icon: "/icon.png"
  }
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  viewportFit: "cover",
  themeColor: "#0e1116"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>
        <ServiceWorkerRegister />
        {children}
      </body>
    </html>
  );
}
