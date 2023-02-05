import React, { useState, useEffect } from 'react';
import { Area, AreaChart, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { format, parseISO, subDays} from "date-fns"


const data = [];
for (let num = 30; num >= 0; num--){
  data.push({
    date: subDays(new Date(), num).toISOString().substring(0,10),
    value: 1+Math.random(),
  })
}

export default function Home(){
  <ResponsiveContainer width={700} height={400}>
    <AreaChart data={data}>
      <Area dataKey="value" />
      <XAxis dataKey="data" />

    </AreaChart>
  </ResponsiveContainer> 
  //return <pre>{JSON.stringify(data, null, 2)}</pre>
}