package net.cpbackend.service;

import org.springframework.stereotype.Service;
import net.cpbackend.model.Stanza;
import net.cpbackend.repository.IStanzaRepository;

@Service
public class StanzaService extends BaseCrudService<Stanza, IStanzaRepository> {
}

