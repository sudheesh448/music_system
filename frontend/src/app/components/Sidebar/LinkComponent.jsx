

export default function LinkButton ({title, icon}) {
    return (
        <><button className="focus-visible:ring-ring gap-2 bg-secondary text-secondary-foreground hover:bg-secondary/80 inline-flex h-9 w-full items-center justify-start whitespace-nowrap rounded-md px-4 py-3 text-xl hover:bg-gray-700 font-medium shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 disabled:pointer-events-none disabled:opacity-50">
        {icon}
        {title}
      </button></>
    )
}