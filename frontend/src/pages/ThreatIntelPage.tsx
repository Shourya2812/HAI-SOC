import React, { useState, useEffect } from 'react';
import { socService } from '../api/socService';
import { ThreatIntelFeed } from '../types/index';
import { DashboardCard } from '../components/cards/DashboardCard';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { ShieldAlert, Globe, ExternalLink, ShieldCheck } from 'lucide-react';

export const ThreatIntelPage: React.FC = () => {
  const [intel, setIntel] = useState<ThreatIntelFeed[]>([
    {
      id: 'IOC-001',
      indicator: '192.168.1.105 (Ransomware C2)',
      type: 'IP_ADDRESS',
      threatGroup: 'UNC2452 / APT29',
      description: 'CISA Alert AA24-102A: Active command and control infrastructure targeting PACS imaging servers.',
      riskScore: 92,
      status: 'ACTIVE_BLOCK',
      lastSeen: '10 mins ago',
    },
    {
      id: 'IOC-002',
      indicator: 'phishing-epic-portal.com',
      type: 'DOMAIN',
      threatGroup: 'FIN12 Healthcare Threat Group',
      description: 'Credential harvesting domain spoofing Epic Hyperspace single sign-on authentication portal.',
      riskScore: 85,
      status: 'MONITORED',
      lastSeen: '1 hour ago',
    },
  ]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Static threat indicators (Backend Threat Intel feed integration pending future release)
    setLoading(false);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
            <ShieldAlert className="w-6 h-6 text-red-400" />
            Healthcare Threat Intelligence Feeds
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Global threat indicators (IOCs) targeting hospital networks, EHR platforms, and IoMT devices.
          </p>
        </div>
      </div>

      <DashboardCard
        title="Active Threat Indicators (IOCs)"
        subtitle="Cross-referenced against Health-ISAC and CISA Healthcare Advisories"
      >
        {loading ? (
          <LoadingSkeleton rows={6} />
        ) : (
          <div className="space-y-4">
            {intel.map((feed) => (
              <div
                key={feed.id}
                className="p-4 bg-slate-950/80 border border-slate-800 rounded-xl space-y-3 hover:border-slate-700 transition-colors"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="p-1.5 rounded-lg bg-red-950/80 border border-red-800/60 text-red-400 font-mono text-xs font-bold">
                      {feed.type}
                    </span>
                    <span className="font-mono text-sm font-bold text-cyan-400">{feed.indicator}</span>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-950 text-amber-400 border border-amber-800/60">
                      Risk Score: {feed.riskScore}/100
                    </span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-purple-950 text-purple-300 border border-purple-800/60">
                      {feed.status}
                    </span>
                  </div>
                </div>

                <p className="text-xs text-slate-300">{feed.description}</p>

                <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-900 text-[11px] font-mono text-slate-400">
                  <span className="flex items-center gap-1 text-slate-300">
                    <Globe className="w-3 h-3 text-cyan-400" />
                    Threat Group: <strong>{feed.threatGroup}</strong>
                  </span>
                  <span>Last Seen: {feed.lastSeen}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </DashboardCard>
    </div>
  );
};
