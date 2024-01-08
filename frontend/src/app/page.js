"use client";

import MusicPlayer from "./components/MusicPlayer/MusicPlayer";
import { VscAdd } from "react-icons/vsc";
import { FiFolder, FiList } from "react-icons/fi";
import { SlMusicToneAlt } from "react-icons/sl";
import { useState } from "react";
import AddMusicModal from "./components/AddMusic/AddMusicModal";

export default function Home() {
  const [listType, setListType] = useState("Musics");
  return (
    <div className="h-full px-4 py-6 lg:px-8">
      <div dir="ltr" data-orientation="horizontal" className="h-full space-y-6">
        <div className=" justify-end rounded-lg py-3  flex items-center">
          <div className=" px-4">
            <AddMusicModal />
          </div>
        </div>
        <div className="flex ">
          <div className="w-full">
            <MusicPlayer />
          </div>
          <div className=" w-full p-3">
            <div className=" w-1/2 text-2xl font-bold flex items-center justify-between gap-2 mb-2">
              <div className="flex items-center gap-2 transition-all duration-100">
                <FiList color="red" />
                {listType}
              </div>
              <div className=" flex gap-2 items-center">
                <div
                  onClick={() => setListType("Albums")}
                  className={`hover:bg-gray-200 text-xs flex items-center gap-2 p-1 hover:text-black rounded-full px-2 cursor-pointer transition-all ${
                    listType === "Albums" && "bg-gray-200 text-black"
                  }`}
                >
                  <FiFolder size={15} title="Albums" />
                  Albums
                </div>

                <div
                  onClick={() => setListType("Musics")}
                  className={`hover:bg-gray-200 text-xs flex items-center gap-2 p-1 hover:text-black rounded-full px-2 cursor-pointer transition-all ${
                    listType === "Musics" && "bg-gray-200 text-black"
                  }`}
                >
                  <SlMusicToneAlt size={15} title="Musics" />
                  Albums
                </div>
              </div>
            </div>

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
