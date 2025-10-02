import type { Metadata } from "next";
import { Bricolage_Grotesque, Darker_Grotesque, Montserrat, Poppins } from "next/font/google";
import "./globals.css";

const bricolageGrotesque = Bricolage_Grotesque({
  subsets: ["latin"],
  variable: "--font-bricolage",
});

const darkerGrotesque = Darker_Grotesque({
  subsets: ["latin"],
  variable: "--font-darker-grotesque",
});

const montserrat = Montserrat({
  subsets: ["latin"],
  variable: "--font-montserrat",
});

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["100", "200", "300", "400", "500", "600", "700", "800", "900"],
  variable: "--font-poppins",
});

export const metadata: Metadata = {
  title: "Urban Flood Risk Analytics Portal - Team Codezilla",
  description: "A Next.js landing page with animated background that connects to the Urban Flood Risk Analytics dashboard.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${bricolageGrotesque.variable} ${darkerGrotesque.variable} ${montserrat.variable} ${poppins.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}