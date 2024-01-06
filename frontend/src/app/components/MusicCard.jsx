export default function MusicCard () {
    return (<> <div className="w-[250px] bg-gray-700 rounded-lg space-y-3">
    <span data-state="closed">
      <div className="overflow-hidden rounded-md">
        <img
          alt="React Rendezvous"
          loading="lazy"
          width="250"
          height="330"
          decoding="async"
          data-nimg="1"
          className="aspect-[3/4] h-auto w-auto object-cover transition-all hover:scale-105"
          srcSet="/_next/image?url=https%3A%2F%2Fimages.unsplash.com%2Fphoto-1611348586804-61bf6c080437%3Fw%3D300%26dpr%3D2%26q%3D80&amp;w=256&amp;q=75 1x, /_next/image?url=https%3A%2F%2Fimages.unsplash.com%2Fphoto-1611348586804-61bf6c080437%3Fw%3D300%26dpr%3D2%26q%3D80&amp;w=640&amp;q=75 2x"
          src="/_next/image?url=https%3A%2F%2Fimages.unsplash.com%2Fphoto-1611348586804-61bf6c080437%3Fw%3D300%26dpr%3D2%26q%3D80&amp;w=640&amp;q=75"
          style={{"color": "transparent;"}}
        />
      </div>
    </span>
    <div className="space-y-1 text-sm">
      <h3 className="font-medium leading-none">
        React Rendezvous
      </h3>
      <p className="text-muted-foreground text-xs">
        Ethan Byte
      </p>
    </div>
  </div></>)
}