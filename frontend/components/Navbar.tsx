import { FC } from "react";
import Image from "next/image";
import Link from "next/link";
import {
    NavigationMenu,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu"
import logo from "@/public/logo.png";

const Navbar: FC = () => {
    return (
        <nav className="w-full bg-gray-900 text-white px-4 py-2 fixed top-0 z-50">
            <div className="container flex justify-between">
                <NavigationMenu>
                    <NavigationMenuList className="space-x-3">
                        <NavigationMenuItem>
                            <Link href="/" passHref>
                                <Image src={logo} alt="Logo" width={40} height={40} className="cursor-pointer" />
                            </Link>
                        </NavigationMenuItem>
                        <NavigationMenuItem>
                            <Link href="/" legacyBehavior passHref>
                                <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                                    Servers
                                </NavigationMenuLink>
                            </Link>
                        </NavigationMenuItem>
                        <NavigationMenuItem>
                            <Link href="/" legacyBehavior passHref>
                                <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                                    Playsets
                                </NavigationMenuLink>
                            </Link>
                        </NavigationMenuItem>
                    </NavigationMenuList>
                </NavigationMenu>
            </div>
        </nav >
    );
};

export default Navbar;