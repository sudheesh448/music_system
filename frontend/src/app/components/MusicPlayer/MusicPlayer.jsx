import React from "react";
import { FcLike, FcLikePlaceholder } from "react-icons/fc";
import { FiSkipBack, FiSkipForward, FiPlay } from "react-icons/fi";

export default function MusicPlayer() {
  return (
    <>
      <div class=" dark:transparent p-5  items-center">
        <div class=" bg-white rounded-lg px-4 py-2 dark:backdrop-blur-xl">
          <div class="px-10 pt-10 pb-4 flex items-center z-50">
            <img
              data-amplitude-song-info="cover_art_url"
              class="w-24 h-24 rounded-md mr-6 border border-bg-player-light-background dark:border-cover-dark-border"
            />

            <div class="flex flex-col">
              <span
                data-amplitude-song-info="name"
                class="font-sans text-lg font-medium leading-7 text-slate-900 dark:text-white"
              ></span>
              <span
                data-amplitude-song-info="artist"
                class="font-sans text-base font-medium leading-6 text-gray-500 dark:text-gray-400"
              ></span>
              <span
                data-amplitude-song-info="album"
                class="font-sans text-base font-medium leading-6 text-gray-500 dark:text-gray-400"
              ></span>
            </div>
          </div>
          <div class="w-full flex flex-col px-10 pb-6 z-50">
            <input
              type="range"
              id="song-percentage-played"
              class="amplitude-song-slider mb-3"
              step=".1"
            />
            <div class="flex w-full justify-between">
              <span class="amplitude-current-time text-xs font-sans tracking-wide font-medium text-sky-500 dark:text-sky-300"></span>
              <span class="amplitude-duration-time text-xs font-sans tracking-wide font-medium text-gray-500"></span>
            </div>
          </div>

          <div class="rounded-b-xl  border-t gap-4 p-4 border-gray-200 flex items-center justify-center z-50 dark:bg-control-panel-dark-background dark:border-gray-900">
            <div className=" hover:bg-gray-300 transition-all flex items-center place-content-center pe-1 rounded-full h-10 w-10">
              <FcLike size={25} />
            </div>
            {/* <FcLikePlaceholder size={25}  /> */}

            <div className=" bg-gray-300 py-1 rounded-md flex items-center px-6 gap-3">
              <div className=" hover:bg-gray-200 transition-all flex items-center place-content-center rounded-full h-10 w-10">
                <FiSkipBack color="gray" size={25} />
              </div>

              <div className=" hover:bg-gray-200 transition-all flex items-center place-content-center rounded-full h-10 w-10">
                <FiPlay color="gray" size={25} />
              </div>
              <div className=" hover:bg-gray-200 transition-all flex items-center place-content-center rounded-full h-10 w-10">
                <FiSkipForward color="gray" size={25} />
              </div>
            </div>
          </div>
        </div>
        {/* <div class="flex items-center justify-center mt-10">
				<a class="text-xs leading-5 font-medium text-sky-600 dark:text-sky-400 bg-sky-400/10 rounded-full py-1 px-3 flex items-center hover:bg-sky-400/20" target="_blank" href="https://tailwindcss.com/">
					Designed With: <strong class="font-semibold">Tailwind CSS v3.0</strong><svg width="3" height="6" class="ml-3 overflow-visible text-sky-300 dark:text-sky-400" aria-hidden="true"><path d="M0 0L3 3L0 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>
				</a>

				<a class="ml-5 text-xs leading-5 font-medium text-emerald-600 dark:text-emerald-400 bg-emerald-400/10 rounded-full py-1 px-3 flex items-center hover:bg-emerald-400/20" target="_blank" href="https://github.com/serversideup/amplitudejs">
					Functionality By: <strong class="font-semibold">AmplitudeJS v5.2</strong><svg width="3" height="6" class="ml-3 overflow-visible text-emerald-300 dark:text-emerald-400" aria-hidden="true"><path d="M0 0L3 3L0 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>
				</a>
			</div> */}
      </div>
    </>
  );
}
