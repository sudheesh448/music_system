import LinkButton from "./LinkComponent";
import { FaMusic } from "react-icons/fa";
import { BiAlbum } from "react-icons/bi";

export default function Sidebar () {
    return (
        <><div className="hidden pb-12 lg:block">
        <div className="space-y-4 py-4">
          <div className="px-3 py-2">
            <h2 className="mb-2 px-4 text-4xl font-semibold tracking-tight">
              Discover
            </h2>
            <div className="space-y-1 mt-4">
              <LinkButton title="Songs" icon={<FaMusic />}  />
              <LinkButton title="Albums" icon={<BiAlbum />} />
            </div>
          </div>
        </div>
      </div></>
    )
}