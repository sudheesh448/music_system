export default function Button ({title}) {
    return (
        <>              <button
        type="button"
        role="menuitem"
        id="radix-:r2i:"
        aria-haspopup="menu"
        aria-expanded="false"
        data-state="closed"
        className="focus:bg-accent focus:text-accent-foreground data-[state=open]:bg-accent data-[state=open]:text-accent-foreground flex cursor-default select-none items-center rounded-sm px-3 py-1 text-sm font-bold outline-none"
        tabindex="-1"
        data-orientation="horizontal"
        data-radix-collection-item=""
      >
        Music
      </button></>
    )
}