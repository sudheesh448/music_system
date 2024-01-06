import Image from "next/image";
import MusicCard from "./components/MusicCard";
import MusicPlayer from "./components/MusicPlayer/MusicPlayer";
import { VscAdd } from "react-icons/vsc";
import { FiList } from "react-icons/fi";

export default function Home() {
  return (
    <div className="h-full px-4 py-6 lg:px-8">
      <div dir="ltr" data-orientation="horizontal" className="h-full space-y-6">
        <div className=" justify-end rounded-lg py-3  flex items-center">
          <div className=" px-4">
            <button className="text-xl text-gray-700 hover:bg-gray-200 transition-all  px-4 py-2 flex gap-2 items-center rounded-md bg-white">
              <VscAdd />
              Add music
            </button>
          </div>
        </div>
        <div className="flex ">
          <div className="w-full">
            <MusicPlayer />
          </div>
          <div className=" w-full p-3">
            <div className=" text-2xl font-bold flex items-center gap-2 mb-2"><FiList />Music list</div>
            <div className="">
              <div className=" w-1/2 mb-2  rounded-lg py-2 px-3 bg-white text-gray-500">
                Music here
              </div>
              <div className=" w-1/2 mb-2  rounded-lg py-2 px-3 bg-white text-gray-500">
                Music here
              </div>
              <div className=" w-1/2 mb-2  rounded-lg py-2 px-3 bg-white text-gray-500">
                Music here
              </div>
              <div className=" w-1/2 mb-2  rounded-lg py-2 px-3 bg-white text-gray-500">
                Music here
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
