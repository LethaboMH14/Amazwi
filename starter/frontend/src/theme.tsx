import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
export type Theme = "midnight" | "daylight" | "ndebele";
export function isNdebeleSeason(date=new Date(), search="") { return date.getMonth()===8 || new URLSearchParams(search).get("season")==="heritage"; }
const ThemeContext=createContext<{theme:Theme;setTheme:(theme:Theme)=>void}>({theme:"midnight",setTheme:()=>{}});
export function ThemeProvider({children}:{children:ReactNode}){const [theme,setTheme]=useState<Theme>(()=>{const saved=localStorage.getItem("amazwi.theme");return saved==="midnight"?"midnight":"daylight";});useEffect(()=>{document.documentElement.dataset.theme=theme;if(theme!=="ndebele")localStorage.setItem("amazwi.theme",theme);},[theme]);return <ThemeContext.Provider value={{theme,setTheme}}>{children}</ThemeContext.Provider>;}
export function ThemeControl(){const {theme,setTheme}=useContext(ThemeContext);return <label>Theme <select value={theme} onChange={e=>setTheme(e.target.value as Theme)}><option value="midnight">Midnight Shweshwe</option><option value="daylight">Signal Daylight</option>{isNdebeleSeason()&&<option value="ndebele">Ndebele Heritage</option>}</select></label>;}
export const useTheme=()=>useContext(ThemeContext);
