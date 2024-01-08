import { Inter } from "next/font/google";
import "./globals.css";
import Sidebar from "./components/Sidebar/SidenavBar";
import bg from "../../public/bg.jpg"
import bg2 from "../../public/bg-2.jpg"
const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className + " relative bg-gradient-to-r text-white from-violet-500 to-purple-500"} style={{backgroundImage : `url(${bg2.src})` }}>
        <div className="absolute h-screen -z-10 w-full bg-gradient-to-t from-black from-40%"></div>
        <div className=" overflow-hidden rounded-[0.5rem] ">
          <div className="md:hidden">
            <img
              alt="Music"
              loading="lazy"
              width="1280"
              height="1114"
              decoding="async"
              data-nimg="1"
              className="block dark:hidden"
              srcSet="/_next/image?url=%2Fexamples%2Fmusic-light.png&amp;w=1920&amp;q=75 1x, /_next/image?url=%2Fexamples%2Fmusic-light.png&amp;w=3840&amp;q=75 2x"
              src="/_next/image?url=%2Fexamples%2Fmusic-light.png&amp;w=3840&amp;q=75"
              style={{"color": "transparent"}}
            />
            <img
              alt="Music"
              loading="lazy"
              width="1280"
              height="1114"
              decoding="async"
              data-nimg="1"
              className="hidden dark:block"
              srcSet="/_next/image?url=%2Fexamples%2Fmusic-dark.png&amp;w=1920&amp;q=75 1x, /_next/image?url=%2Fexamples%2Fmusic-dark.png&amp;w=3840&amp;q=75 2x"
              src="/_next/image?url=%2Fexamples%2Fmusic-dark.png&amp;w=3840&amp;q=75"
              style={{"color": "transparent;"}}
            />
          </div>
          <div className="hidden md:block">
            <div className="">
              <div className="">
                <div className="grid lg:grid-cols-5 h-screen">
                  {<Sidebar />}
                  <div className="col-span-3 lg:col-span-4 ">
                  {children}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </body>
    </html>
  );
}