export default function Logo() {
  return (
    <div className="flex items-center gap-2">
      <svg width="38" height="38" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="ghGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#00F5D4" />
            <stop offset="100%" stopColor="#7A5CFF" />
          </linearGradient>
        </defs>
        <rect x="8" y="8" width="104" height="104" rx="20" stroke="url(#ghGrad)" strokeWidth="8" />
        <path d="M32 60C32 44 43 32 60 32H76V44H60C50 44 44 50 44 60C44 70 50 76 60 76H76V88H60C43 88 32 76 32 60Z" fill="url(#ghGrad)" />
        <path d="M84 32H96V88H84V66H60V54H84V32Z" fill="url(#ghGrad)" />
      </svg>
      <span className="font-semibold tracking-wide">GH Pvt Ltd</span>
    </div>
  );
}
