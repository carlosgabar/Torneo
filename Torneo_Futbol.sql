PGDMP         2                |            Torneo_Futbol    15.1    15.1 $    3           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            4           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            5           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            6           1262    25425    Torneo_Futbol    DATABASE     �   CREATE DATABASE "Torneo_Futbol" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Spain.1252';
    DROP DATABASE "Torneo_Futbol";
                postgres    false            �            1259    41919    admin    TABLE     K   CREATE TABLE public.admin (
    "user" text NOT NULL,
    password text
);
    DROP TABLE public.admin;
       public         heap    postgres    false            �            1259    41809    equipo_id_seq    SEQUENCE     v   CREATE SEQUENCE public.equipo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.equipo_id_seq;
       public          postgres    false            �            1259    25440    equipo    TABLE     �   CREATE TABLE public.equipo (
    "ID_equipo" integer DEFAULT nextval('public.equipo_id_seq'::regclass) NOT NULL,
    "ID_categoria" integer NOT NULL,
    "Nombre_equipo" character varying(40)
);
    DROP TABLE public.equipo;
       public         heap    postgres    false    219            �            1259    41926    id_jugador_seq    SEQUENCE     w   CREATE SEQUENCE public.id_jugador_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.id_jugador_seq;
       public          postgres    false            �            1259    41831    id_partido_seq    SEQUENCE     w   CREATE SEQUENCE public.id_partido_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.id_partido_seq;
       public          postgres    false            �            1259    25433    jugador    TABLE     �   CREATE TABLE public.jugador (
    "ID_jugador" integer NOT NULL,
    "Nombre" character varying(50),
    "ID_equipo" integer NOT NULL,
    "ID_torneo" integer,
    goles integer DEFAULT 0
);
    DROP TABLE public.jugador;
       public         heap    postgres    false            �            1259    25460    partidos    TABLE     �   CREATE TABLE public.partidos (
    "ID_partido" integer NOT NULL,
    "ID_local" integer,
    "ID_visitante" integer,
    "ID_torneo" integer,
    "ID_ganador" integer
);
    DROP TABLE public.partidos;
       public         heap    postgres    false            �            1259    33618    torneo_id_seq    SEQUENCE     v   CREATE SEQUENCE public.torneo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.torneo_id_seq;
       public          postgres    false            �            1259    25426    torneo    TABLE     �   CREATE TABLE public.torneo (
    "ID_torneo" integer DEFAULT nextval('public.torneo_id_seq'::regclass) NOT NULL,
    "Nombre_torneo" character varying(30),
    "Nro_Categoria" integer,
    "Nro_equipos" integer
);
    DROP TABLE public.torneo;
       public         heap    postgres    false    218            �            1259    41816    torneo_equipo    TABLE     }  CREATE TABLE public.torneo_equipo (
    "ID_equipo" integer NOT NULL,
    "ID_torneo" integer NOT NULL,
    gfavor_equipo integer DEFAULT 0,
    gcontra_equipo integer DEFAULT 0,
    "Puntos" integer DEFAULT 0,
    victorias integer DEFAULT 0,
    derrotas integer DEFAULT 0,
    empates integer DEFAULT 0,
    cantidadjugados integer DEFAULT 0,
    dif_goles integer DEFAULT 0
);
 !   DROP TABLE public.torneo_equipo;
       public         heap    postgres    false            /          0    41919    admin 
   TABLE DATA           1   COPY public.admin ("user", password) FROM stdin;
    public          postgres    false    222   ~)       )          0    25440    equipo 
   TABLE DATA           N   COPY public.equipo ("ID_equipo", "ID_categoria", "Nombre_equipo") FROM stdin;
    public          postgres    false    216   �)       (          0    25433    jugador 
   TABLE DATA           Z   COPY public.jugador ("ID_jugador", "Nombre", "ID_equipo", "ID_torneo", goles) FROM stdin;
    public          postgres    false    215   �)       *          0    25460    partidos 
   TABLE DATA           g   COPY public.partidos ("ID_partido", "ID_local", "ID_visitante", "ID_torneo", "ID_ganador") FROM stdin;
    public          postgres    false    217   *       '          0    25426    torneo 
   TABLE DATA           ^   COPY public.torneo ("ID_torneo", "Nombre_torneo", "Nro_Categoria", "Nro_equipos") FROM stdin;
    public          postgres    false    214   k*       -          0    41816    torneo_equipo 
   TABLE DATA           �   COPY public.torneo_equipo ("ID_equipo", "ID_torneo", gfavor_equipo, gcontra_equipo, "Puntos", victorias, derrotas, empates, cantidadjugados, dif_goles) FROM stdin;
    public          postgres    false    220   �*       7           0    0    equipo_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.equipo_id_seq', 4, true);
          public          postgres    false    219            8           0    0    id_jugador_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.id_jugador_seq', 1, true);
          public          postgres    false    223            9           0    0    id_partido_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.id_partido_seq', 12, true);
          public          postgres    false    221            :           0    0    torneo_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.torneo_id_seq', 1, true);
          public          postgres    false    218            �           2606    25444    equipo Equipo_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.equipo
    ADD CONSTRAINT "Equipo_pkey" PRIMARY KEY ("ID_equipo");
 >   ALTER TABLE ONLY public.equipo DROP CONSTRAINT "Equipo_pkey";
       public            postgres    false    216            �           2606    25439    jugador Jugador_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.jugador
    ADD CONSTRAINT "Jugador_pkey" PRIMARY KEY ("ID_jugador");
 @   ALTER TABLE ONLY public.jugador DROP CONSTRAINT "Jugador_pkey";
       public            postgres    false    215            �           2606    25464    partidos Partidos_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.partidos
    ADD CONSTRAINT "Partidos_pkey" PRIMARY KEY ("ID_partido");
 B   ALTER TABLE ONLY public.partidos DROP CONSTRAINT "Partidos_pkey";
       public            postgres    false    217            �           2606    25432    torneo Torneo_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.torneo
    ADD CONSTRAINT "Torneo_pkey" PRIMARY KEY ("ID_torneo");
 >   ALTER TABLE ONLY public.torneo DROP CONSTRAINT "Torneo_pkey";
       public            postgres    false    214            �           2606    41925    admin admin_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY ("user");
 :   ALTER TABLE ONLY public.admin DROP CONSTRAINT admin_pkey;
       public            postgres    false    222            �           2606    41820     torneo_equipo torneo_equipo_pkey 
   CONSTRAINT     t   ALTER TABLE ONLY public.torneo_equipo
    ADD CONSTRAINT torneo_equipo_pkey PRIMARY KEY ("ID_equipo", "ID_torneo");
 J   ALTER TABLE ONLY public.torneo_equipo DROP CONSTRAINT torneo_equipo_pkey;
       public            postgres    false    220    220            �           2606    25450    jugador ID_equipo    FK CONSTRAINT     �   ALTER TABLE ONLY public.jugador
    ADD CONSTRAINT "ID_equipo" FOREIGN KEY ("ID_equipo") REFERENCES public.equipo("ID_equipo") NOT VALID;
 =   ALTER TABLE ONLY public.jugador DROP CONSTRAINT "ID_equipo";
       public          postgres    false    215    3212    216            �           2606    41821    torneo_equipo ID_equipo    FK CONSTRAINT     �   ALTER TABLE ONLY public.torneo_equipo
    ADD CONSTRAINT "ID_equipo" FOREIGN KEY ("ID_equipo") REFERENCES public.equipo("ID_equipo");
 C   ALTER TABLE ONLY public.torneo_equipo DROP CONSTRAINT "ID_equipo";
       public          postgres    false    216    220    3212            �           2606    25465    partidos ID_local    FK CONSTRAINT     �   ALTER TABLE ONLY public.partidos
    ADD CONSTRAINT "ID_local" FOREIGN KEY ("ID_local") REFERENCES public.equipo("ID_equipo") NOT VALID;
 =   ALTER TABLE ONLY public.partidos DROP CONSTRAINT "ID_local";
       public          postgres    false    216    217    3212            �           2606    41826    torneo_equipo ID_torneo    FK CONSTRAINT     �   ALTER TABLE ONLY public.torneo_equipo
    ADD CONSTRAINT "ID_torneo" FOREIGN KEY ("ID_torneo") REFERENCES public.torneo("ID_torneo");
 C   ALTER TABLE ONLY public.torneo_equipo DROP CONSTRAINT "ID_torneo";
       public          postgres    false    3208    220    214            �           2606    41927    jugador ID_torneo    FK CONSTRAINT     �   ALTER TABLE ONLY public.jugador
    ADD CONSTRAINT "ID_torneo" FOREIGN KEY ("ID_torneo") REFERENCES public.torneo("ID_torneo") NOT VALID;
 =   ALTER TABLE ONLY public.jugador DROP CONSTRAINT "ID_torneo";
       public          postgres    false    3208    215    214            �           2606    25470    partidos ID_visitante    FK CONSTRAINT     �   ALTER TABLE ONLY public.partidos
    ADD CONSTRAINT "ID_visitante" FOREIGN KEY ("ID_visitante") REFERENCES public.equipo("ID_equipo") NOT VALID;
 A   ALTER TABLE ONLY public.partidos DROP CONSTRAINT "ID_visitante";
       public          postgres    false    216    3212    217            /      x�KL����L�KL�I54261����� Z+      )   +   x�3�44���,�21����A���<.#9���+F��� ��		      (      x�3�H-H�4Bc�=... #�'      *   K   x�-���0�w=jh)�t�9p?��,�Ѣ���a���T&^�(.҅[���^xI�K��u%r�{i� ��=[      '      x�3�,(J��L-�44�4����� 9��      -   .   x�3�4�4@�\&X��b�@l�3�4��A�>�p��qqq ��	�     